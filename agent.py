import os
import google.generativeai as genai
from openai import OpenAI

# --- CONFIGURATION: TIGHTLY COUPLED MODELS ---
# This dictionary controls the specific model used for each provider.
# To change a model version, update it here once.
LLM_CONFIG = {
    "google": {
        "provider": "Google",
        "model_name": "gemini-1.5-flash", 
        "display_name": "Google Gemini (Flash)"
    },
    "github": {
        "provider": "GitHub",
        "model_name": "gpt-4o",
        "display_name": "GitHub Models (GPT-4o)"
    },
    "huggingface": {
        "provider": "HuggingFace",
        "model_name": "meta-llama/Meta-Llama-3-8B-Instruct",
        "display_name": "Hugging Face (Llama 3)"
    }
}

def get_llm_response(config_key, full_prompt, system_role):
    """
    Dispatcher that looks up the provider/model details from the config key.
    """
    # 1. Load Configuration
    config = LLM_CONFIG.get(config_key)
    if not config:
        return f"Error: Configuration '{config_key}' not found."
    
    provider = config["provider"]
    model_name = config["model_name"]

    try:
        # --- GOOGLE GEMINI ---
        if provider == "Google":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel(model_name)
            combined_prompt = f"{system_role}\n\n{full_prompt}"
            response = model.generate_content(combined_prompt)
            return response.text

        # --- GITHUB MODELS (Free GPT-4o) ---
        elif provider == "GitHub":
            client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=os.getenv("GITHUB_TOKEN")
            )
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=1.0,
                max_tokens=4096,
            )
            return response.choices[0].message.content

        # --- HUGGING FACE ---
        elif provider == "HuggingFace":
            client = OpenAI(
                base_url="https://router.huggingface.co/v1",
                api_key=os.getenv("HF_TOKEN")
            )
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=4096,
            )
            return response.choices[0].message.content
        
        else:
            return f"Error: Provider {provider} not supported."

    except Exception as e:
        return f"Error with {provider}: {str(e)}"

def generate_sales_insights(product_name, product_category, value_prop, target_customer, 
                            company_data, competitor_data_list, product_manual_text=None,
                            llm_choice="google", 
                            system_instruction=None):
    
    # 1. Prepare Data Context
    competitor_text = "\n".join(competitor_data_list) if competitor_data_list else "None"
    manual_context = f"\nMANUAL:\n{product_manual_text}" if product_manual_text else ""

    # 2. Build Data Prompt
    data_context = f"""
    --- DATA CONTEXT ---
    PRODUCT: {product_name} ({product_category})
    VALUE PROP: {value_prop}
    CUSTOMER: {target_customer}
    {manual_context}

    TARGET DATA: {company_data[:10000]}
    COMPETITOR DATA: {competitor_text}
    """

    if not system_instruction:
        system_instruction = """
        You are an expert Sales Assistant Agent.
        Generate a "One-Pager" sales insight document.
        Include: Strategy, Competitors, Leadership, and Sales Pitch.
        EXTRACT LINKS: List any relevant URLs found in the text.
        """

    # 3. Call Dispatcher
    response = get_llm_response(llm_choice, data_context, system_instruction)
    
    # Return text AND the friendly name for the UI
    return response, LLM_CONFIG[llm_choice]["display_name"]

def refine_sales_insights(draft_content, original_data_context, previous_llm_choice):
    """
    CHAIN STEP 2: The Cross-Model Editor.
    Routes the draft to the strongest possible 'Senior Editor' model.
    """
    
    # STRATEGY: Always route to the smartest model (GPT-4o), 
    # unless GPT-4o wrote the draft.
    
    if previous_llm_choice == "github":
        # If GPT-4o wrote it, get a second opinion from Gemini (Peer Review)
        editor_choice = "google"
    else:
        # For everyone else (Gemini Flash, Llama 3), escalate to GPT-4o (The Boss)
        editor_choice = "github"
        
    system_role = "You are a Senior Editor. Verify accuracy, tone, and citations."
    
    refine_prompt = f"""
    ORIGINAL SOURCE DATA:
    {original_data_context[:10000]}
    
    DRAFT INSIGHTS (To be Critiqued):
    {draft_content}
    
    TASK:
    1. Verify that all claims in the Draft are supported by the Source Data.
    2. CRITICAL: If the Draft is missing "Article Links" or citations found in the Source Data, ADD THEM NOW.
    3. Ensure the tone is professional and persuasive.
    4. Output the final, polished Markdown document.
    """
    
    # Note: Ensure your LLM_CONFIG['google'] points to 'gemini-1.5-pro' if possible 
    # for the best peer review experience.
    
    response = get_llm_response(editor_choice, refine_prompt, system_role)
    return response, LLM_CONFIG[editor_choice]["display_name"]
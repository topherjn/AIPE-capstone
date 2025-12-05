import os
import google.generativeai as genai
from openai import OpenAI


def get_llm_response(provider, model_name, full_prompt, system_role):
    """
    Dispatcher function to handle Google (Native) and GitHub (OpenAI-Compatible).
    """
    try:
        # --- GOOGLE GEMINI ---
        if provider == "Google":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel(model_name)
            
            # Gemini creates a unified context by joining system + user
            combined_prompt = f"{system_role}\n\n{full_prompt}"
            response = model.generate_content(combined_prompt)
            return response.text

        # --- GITHUB MODELS (Free GPT-4o) ---
        elif provider == "GitHub":
            # GitHub Models uses the OpenAI SDK but points to Azure
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
        
        # --- HUGGING FACE (New) ---
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
                            # V2 Arguments
                            provider="Google", 
                            model_name="gemini-2.5-pro",
                            system_instruction=None):
    
    # 1. Prepare Data Context
    competitor_text = "\n".join(competitor_data_list) if competitor_data_list else "None"
    manual_context = f"\nMANUAL:\n{product_manual_text}" if product_manual_text else ""

    # 2. Build the Data Prompt
    data_context = f"""
    --- DATA CONTEXT ---
    PRODUCT: {product_name} ({product_category})
    VALUE PROP: {value_prop}
    CUSTOMER: {target_customer}
    {manual_context}

    TARGET COMPANY DATA:
    {company_data[:10000]}

    COMPETITOR DATA:
    {competitor_text}
    """

    # 3. Use default instruction if none provided
    if not system_instruction:
        system_instruction = """
        You are an expert Sales Assistant Agent.
        Generate a "One-Pager" sales insight document based on the provided data.
        Include: Strategy Analysis, Competitor Mentions, Leadership, and a Tailored Sales Pitch.
        """

    # 4. Call Dispatcher
    return get_llm_response(provider, model_name, data_context, system_instruction), model_name

def refine_sales_insights(draft_content, original_data_context, provider, model_name):
    """
    CHAIN STEP 2: The Editor.
    Takes the initial draft and the source data, then improves it.
    """
    system_role = "You are a Senior Editor. Your goal is to verify accuracy and improve formatting."
    
    refine_prompt = f"""
    ORIGINAL SOURCE DATA:
    {original_data_context[:10000]}
    
    DRAFT INSIGHTS:
    {draft_content}
    
    TASK:
    1. Verify that all claims in the Draft are supported by the Source Data.
    2. If the Draft is missing "Article Links" or citations found in the Source Data, add them.
    3. Ensure the tone is professional and persuasive.
    4. Output the final polished Markdown.
    """
    
    # Reuse your existing dispatcher
    return get_llm_response(provider, model_name, refine_prompt, system_role)
import google.generativeai as genai
import os

# Define model globally or in a config so it's easy to change
MODEL_NAME = 'gemini-2.5-flash-lite' 

def generate_sales_insights(product_name, product_category, value_prop, target_customer, company_data, competitor_data_list, product_manual_text=None):
    """
    Constructs the prompt and calls the Gemini API.
    Returns a tuple: (insight_text, model_used)
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(MODEL_NAME)

    competitor_text = "\n".join(competitor_data_list) if competitor_data_list else "No competitor data provided."
    
    # Handle optional PDF text
    manual_context = ""
    if product_manual_text:
        manual_context = f"\nADDITIONAL PRODUCT CONTEXT (Uploaded Manual):\n{product_manual_text}\n"

    prompt = f"""
    ROLE: You are an expert Sales Assistant Agent. 
    OBJECTIVE: Generate a "One-Pager" sales insight document.
    
    INPUT DATA:
    - Product: {product_name}
    - Category: {product_category}
    - Value Prop: {value_prop}
    - Target Customer: {target_customer}
    {manual_context}

    SCRAPED TARGET DATA:
    {company_data}

    SCRAPED COMPETITOR DATA:
    {competitor_text}

    OUTPUT FORMAT (Markdown):
    # Account Insights for {target_customer}

    ## 1. Strategy Analysis
    (Relate company strategy to {product_name}. If product manual provided, reference specific features that solve their problems.)

    ## 2. Competitor Mentions
    (Analyze partnerships or competitor mentions.)

    ## 3. Leadership
    (Key people.)

    ## 4. Sales Pitch
    (Tailored pitch. If manual provided, quote specific benefits from it.)
    """

    try:
        response = model.generate_content(prompt)
        return response.text, MODEL_NAME
    except Exception as e:
        return f"Error: {str(e)}", MODEL_NAME
import google.generativeai as genai
import os

def generate_sales_insights(product_name, product_category, value_prop, target_customer, company_data, competitor_data_list):

    """
    Constructs the prompt and calls the Gemini API to generate the one-pager.
    """
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Initialize the model
    # gemini-flash-latest seems to work, may try others
    model = genai.GenerativeModel('gemini-flash-latest')

    # Construct the Competitor String
    competitor_text = "\n".join(competitor_data_list) if competitor_data_list else "No competitor data provided."

    # PROMPT ENGINEERING
    # [cite_start]We use specific constraints to satisfy CAP 931 requirements [cite: 34-37]
    prompt = f"""
    ROLE: You are an expert Sales Assistant Agent. 
    OBJECTIVE: Generate a "One-Pager" sales insight document for a sales representative.
    
    CONSTRAINTS:
    1. Only respond to this specific use case. Do not engage in general conversation.
    2. Base your insights strictly on the provided context (scraped data) and your internal knowledge of the industry.
    3. If the scraped data is insufficient, state that clearly rather than hallucinating specific details.

    INPUT DATA:
    - Product to Sell: {product_name}
    - Product Category: {product_category}
    - Value Proposition: {value_prop}
    - Target Customer Name: {target_customer}

    SCRAPED TARGET COMPANY DATA:
    {company_data}

    SCRAPED COMPETITOR DATA:
    {competitor_text}

    OUTPUT FORMAT (Markdown):
    # Account Insights for {target_customer}

    ## 1. Company Strategy
    (Summarize the company's recent activities, strategic direction, and how they relate to {product_category}. Look for keywords in the text like "strategic", "mission", "upcoming", "focus".)

    ## 2. Competitor Mentions & Analysis
    (Analyze if the company mentions any competitors or has partnerships with them. Compare the scraped competitor data against the target company's needs.)

    ## 3. Leadership Information
    (Identify key leaders mentioned in the text, especially those relevant to {product_category}.)

    ## 4. Sales Angle
    (Based on the {value_prop}, suggest 2-3 specific talking points to pitch {product_name} to this specific company.)

    ## 5. References
    (List any relevant links found in the text.)
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"
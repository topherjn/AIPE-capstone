import streamlit as st
from dotenv import load_dotenv
from scraper import scrape_url
from pdf_handler import extract_text_from_pdf
from agent import generate_sales_insights

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Sales Agent V2", page_icon="💼", layout="wide")

DEFAULT_PROMPT = """
ROLE: You are an expert Sales Assistant Agent.
OBJECTIVE: Generate a comprehensive "One-Pager" sales insight document.

INSTRUCTIONS:
1. Analyze the provided scraped data (in Markdown format).
2. Identify strategic priorities, leadership names, and competitor relationships.
3. Using the user's Value Proposition, craft a specific sales angle.
4. If a Product Manual is provided, cite specific features from it.
5. EXTRACT LINKS: You must list any relevant article links, press releases, or source URLs found in the text.

OUTPUT FORMAT (Markdown):
# Account Insights for {Target Customer}

## 1. Company Strategy
(Summarize active strategy. Cite specific press releases if found.)

## 2. Competitor Analysis
(Mentions of competitors or partnerships.)

## 3. Key Leadership
(Names and titles.)

## 4. Suggested Sales Pitch
(Tailored value prop.)

## 5. References & Article Links
* **List ALL relevant hyperlinks found in the scraped text.**
* Format: `[Title of Article/Page](URL)`
* *If no links are found, explicitely state: "No direct source links were detected in the provided text."*
"""

st.title("💼 Sales Assistant Agent (Hybrid)")
st.markdown("Generate account insights using **Google Gemini**, **GitHub Models (Free Tier)**, or **HuggingFace**.")

# --- 1. ADVANCED SETTINGS (OUTSIDE THE FORM FOR INTERACTIVITY) ---
# We place this here so the 'provider' selection triggers an immediate rerun,
# allowing the 'model_name' to update dynamically.
with st.expander("🛠️ Advanced Settings (Model & Prompt)", expanded=False):
    st.info("Power User Zone: Choose your Brain and customize the Instructions.")
    
    c1, c2 = st.columns(2)
    with c1:
            # Added "HuggingFace" to the list
            provider = st.selectbox("LLM Provider", ["Google", "GitHub", "HuggingFace"])
        
    with c2:
        # Dynamic Default Logic
        if provider == "Google":
            default_model = "gemini-2.5-pro"
            help_text = "Common: gemini-1.5-flash, gemini-2.5-pro"
        elif provider == "GitHub":
            default_model = "gpt-4o"
            help_text = "Free Tier: gpt-4o, gpt-4o-mini, Phi-3-medium-4k-instruct"
        elif provider == "HuggingFace":
                default_model = "meta-llama/Meta-Llama-3-8B-Instruct"
                help_text = "Try: mistralai/Mistral-7B-Instruct-v0.3, microsoft/Phi-3-mini-4k-instruct"
        
        # The 'key' parameter ensures the widget resets when provider changes
        model_name = st.text_input(
            "Model Name", 
            value=default_model, 
            help=help_text,
            key=f"model_name_{provider}"
        )

    system_instruction = st.text_area("System Instructions (Prompt)", value=DEFAULT_PROMPT, height=300)

# --- 2. MAIN INPUT FORM ---
with st.form("input_form"):
    st.header("1. Product & Target Details")
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g., Snowflake Data Cloud")
        product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform")
    with col2:
        target_customer = st.text_input("Target Customer (Name)", placeholder="e.g., John Doe")
        company_url = st.text_input("Target Company URL", placeholder="https://www.target-company.com")
        
    value_proposition = st.text_area("Value Proposition", placeholder="Summarize your product's value...")
    
    st.header("2. Intelligence Sources")
    competitor_urls = st.text_area("Competitor URLs (one per line)", placeholder="https://www.competitor1.com")
    uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=['pdf', 'txt'])

    submitted = st.form_submit_button("Generate Insights")

if submitted:
    if not product_name or not company_url:
        st.warning("Please fill in the Product Name and Target Company URL.")
    else:
        # 1. Scrape Target
        with st.status("Gathering Intelligence...", expanded=True) as status:
            st.write(f"Scraping Target: {company_url}...")
            company_data = scrape_url(company_url)
            
            # 2. Scrape Competitors
            competitor_data_list = []
            if competitor_urls:
                urls_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
                for url in urls_list:
                    st.write(f"Scraping Competitor: {url}...")
                    data = scrape_url(url)
                    competitor_data_list.append(f"Source: {url}\nContent: {data}")
            
            # 3. Process PDF
            product_manual_text = ""
            if uploaded_file:
                st.write("Reading Product Manual...")
                product_manual_text = extract_text_from_pdf(uploaded_file)
            
            # 4. Call AI Agent (Using variables from the 'Advanced Settings' block above)
            st.write(f"Consulting {provider} ({model_name})...")
            
            insights, used_model = generate_sales_insights(
                product_name, 
                product_category, 
                value_proposition, 
                target_customer, 
                company_data, 
                competitor_data_list,
                product_manual_text,
                provider=provider,
                model_name=model_name,
                system_instruction=system_instruction
            )
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # 5. Display Result
        st.caption(f"Generated by: **{provider} / {used_model}**")
        st.divider()
        st.markdown(insights)
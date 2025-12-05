import streamlit as st
import os
from dotenv import load_dotenv
from scraper import scrape_url
from pdf_handler import extract_text_from_pdf
from agent import generate_sales_insights, refine_sales_insights # <--- Imported new function

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Sales Agent V2", page_icon="💼", layout="wide")

DEFAULT_PROMPT = """
ROLE: You are an expert Sales Assistant Agent.
OBJECTIVE: Generate a comprehensive "One-Pager" sales insight document.

INSTRUCTIONS:
1. Analyze the provided scraped data (Markdown).
2. Identify strategic priorities, leadership names, and competitor relationships.
3. Using the user's Value Proposition, craft a specific sales angle.
4. If a Product Manual is provided, cite specific features from it.
5. EXTRACT LINKS: You must list any relevant article links, press releases, or source URLs found in the text.

OUTPUT FORMAT (Markdown):
# Account Insights for {Target Customer}
## 1. Company Strategy
## 2. Competitor Analysis
## 3. Key Leadership
## 4. Suggested Sales Pitch
## 5. References & Article Links
"""

st.title("💼 Sales Assistant Agent (Hybrid)")
st.markdown("Generate account insights using **Google Gemini**, **GitHub Models**, or **Hugging Face**.")

# --- 1. ADVANCED SETTINGS ---
with st.expander("🛠️ Advanced Settings (Model & Prompt)", expanded=False):
    st.info("Power User Zone: Choose your Brain and customize the Instructions.")
    
    c1, c2 = st.columns(2)
    with c1:
        provider = st.selectbox("LLM Provider", ["Google", "GitHub", "HuggingFace"])
        
    with c2:
        if provider == "Google":
            default_model = "gemini-1.5-pro" # Updated based on your feedback
            help_text = "Common: gemini-1.5-pro, gemini-1.5-flash"
        elif provider == "GitHub":
            default_model = "gpt-4o"
            help_text = "Free Tier: gpt-4o, gpt-4o-mini"
        elif provider == "HuggingFace":
            default_model = "meta-llama/Meta-Llama-3-8B-Instruct"
            help_text = "Try: mistralai/Mistral-7B-Instruct-v0.3"
        
        model_name = st.text_input(
            "Model Name", 
            value=default_model, 
            help=help_text,
            key=f"model_name_{provider}"
        )

    system_instruction = st.text_area("System Instructions (Prompt)", value=DEFAULT_PROMPT, height=300)
    
    # NEW: Experiment Toggle
    enable_chaining = st.checkbox("⛓️ Enable Refinement Chain (Experiment D)", 
                                  help="Adds a second LLM pass to verify citations and accuracy.")

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
        with st.status("Gathering Intelligence...", expanded=True) as status:
            st.write(f"Scraping Target: {company_url}...")
            company_data = scrape_url(company_url)
            
            competitor_data_list = []
            if competitor_urls:
                urls_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
                for url in urls_list:
                    st.write(f"Scraping Competitor: {url}...")
                    data = scrape_url(url)
                    competitor_data_list.append(f"Source: {url}\nContent: {data}")
            
            product_manual_text = ""
            if uploaded_file:
                st.write("Reading Product Manual...")
                product_manual_text = extract_text_from_pdf(uploaded_file)
            
            # Step 1: Initial Draft
            st.write(f"Drafting Insights using {provider} ({model_name})...")
            insights, used_model = generate_sales_insights(
                product_name, product_category, value_proposition, target_customer, 
                company_data, competitor_data_list, product_manual_text,
                provider=provider, model_name=model_name, system_instruction=system_instruction
            )
            
            # Step 2: Refinement Chain (Experiment D)
            if enable_chaining:
                st.write("⛓️ Chaining: Editor Mode Active...")
                st.write("Critiquing draft against source data...")
                
                # Reconstruct context for the editor
                competitor_text = "\n".join(competitor_data_list)
                raw_data_context = f"TARGET DATA:\n{company_data}\n\nCOMPETITOR DATA:\n{competitor_text}"
                
                refined_insights = refine_sales_insights(
                    insights, 
                    raw_data_context, 
                    provider, 
                    model_name
                )
                st.write("Polishing final report...")
                insights = refined_insights # Overwrite draft with polished version

            status.update(label="Analysis Complete!", state="complete", expanded=False)

        st.caption(f"Generated by: **{provider} / {used_model}** {'(Refined)' if enable_chaining else ''}")
        st.divider()
        st.markdown(insights)
import streamlit as st
import os
from dotenv import load_dotenv
from scraper import scrape_url
from pdf_handler import extract_text_from_pdf
from agent import generate_sales_insights, refine_sales_insights, LLM_CONFIG

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

st.title("💼 Sales Assistant Agent (V2)")
st.markdown("Generate account insights with **Cross-Model Verification**.")

# --- 1. ADVANCED SETTINGS (Smart Config) ---
with st.expander("🛠️ Advanced Settings (Model & Chain)", expanded=False):
    st.info("Power User Zone: Select your primary drafter. The system will automatically select a different model for verification if chaining is enabled.")
    
    c1, c2 = st.columns(2)
    with c1:
        # Create a mapping of Display Name -> Config Key (e.g. "Google Gemini" -> "google")
        options_map = {v['display_name']: k for k, v in LLM_CONFIG.items()}
        
        # User selects the friendly name
        selected_display_name = st.selectbox("Select Primary AI Model", list(options_map.keys()))
        
        # We retrieve the technical key to pass to the backend
        llm_choice = options_map[selected_display_name]

    with c2:
        # Experiment D Toggle
        enable_chaining = st.checkbox(
            "⛓️ Enable Cross-Model Verification", 
            help="Experiment D: Uses a different AI provider to critique and refine the initial draft."
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
            
            # --- STEP 1: DRAFTING ---
            st.write(f"Drafting Insights using {selected_display_name}...")
            insights, drafter_model_name = generate_sales_insights(
                product_name, product_category, value_proposition, target_customer, 
                company_data, competitor_data_list, product_manual_text,
                llm_choice=llm_choice,
                system_instruction=system_instruction
            )
            
            final_attribution = f"Drafted by: **{drafter_model_name}**"

            # --- STEP 2: REFINEMENT CHAIN (Optional) ---
            if enable_chaining:
                st.write("⛓️ Cross-Verification: Sending to secondary model for critique...")
                
                # Reconstruct context for the editor
                competitor_text = "\n".join(competitor_data_list)
                raw_data_context = f"TARGET DATA:\n{company_data}\n\nCOMPETITOR DATA:\n{competitor_text}"
                
                refined_insights, editor_model_name = refine_sales_insights(
                    insights, 
                    raw_data_context, 
                    llm_choice # Pass previous choice so agent knows to ROTATE
                )
                
                st.write(f"Polishing final report with {editor_model_name}...")
                insights = refined_insights # Overwrite draft
                final_attribution += f" | Verified by: **{editor_model_name}**"

            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # Final Display
        st.caption(final_attribution)
        st.divider()
        st.markdown(insights)
import streamlit as st
import os
from dotenv import load_dotenv
from scraper import scrape_url  # <--- IMPORT THE NEW FUNCTION

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Sales Agent", page_icon="💼")

st.title("💼 Sales Assistant Agent")
st.markdown("Generate account insights, competitor analysis, and strategy summaries.")

with st.form("input_form"):
    st.header("1. Product & Target Details")
    product_name = st.text_input("Product Name", placeholder="e.g., Snowflake Data Cloud")
    product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform")
    value_proposition = st.text_area("Value Proposition", placeholder="Summarize your product's value...")
    target_customer = st.text_input("Target Customer (Name)", placeholder="e.g., John Doe")

    st.header("2. Company Data")
    company_url = st.text_input("Target Company URL", placeholder="https://www.target-company.com")
    # Helper text for competitors
    competitor_urls = st.text_area("Competitor URLs (one per line)", placeholder="https://www.competitor1.com\nhttps://www.competitor2.com")

    uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=['txt', 'pdf', 'md'])

    submitted = st.form_submit_button("Generate Insights")

if submitted:
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: GOOGLE_API_KEY not found in .env file.")
    elif not product_name or not company_url:
        st.warning("Please fill in the Product Name and Target Company URL.")
    else:
        # 1. Scrape Target Company
        with st.spinner(f"Scraping {company_url}..."):
            company_data = scrape_url(company_url)
        
        # 2. Scrape Competitors
        competitor_data = []
        if competitor_urls:
            urls_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
            for url in urls_list:
                with st.spinner(f"Scraping competitor: {url}..."):
                    data = scrape_url(url)
                    competitor_data.append(f"Competitor URL: {url}\nData: {data}")
        
        # 3. Display Data Preview (Debugging Step)
        st.subheader("Data Extraction Preview")
        with st.expander("View Target Company Raw Text"):
            st.write(company_data)
        
        if competitor_data:
            with st.expander("View Competitor Raw Text"):
                st.write("\n---\n".join(competitor_data))
        
        st.success("Scraping complete. Ready for LLM processing.")
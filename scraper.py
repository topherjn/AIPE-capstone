import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# page config
st.set_page_config(page_title="Sales Agent", page_icon="💼")

st.title("💼 Sales Assistant Agent")
st.markdown("Generate account insights, competitor analysis, and strategy summaries.")

# Create a form to keep the UI clean
with st.form("input_form"):
    st.header("1. Product & Target Details")
    
    # Required Inputs per CAP 931 [cite: 43, 46, 49, 50]
    product_name = st.text_input("Product Name", placeholder="e.g., Snowflake Data Cloud")
    product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform")
    value_proposition = st.text_area("Value Proposition", placeholder="Summarize your product's value...")
    target_customer = st.text_input("Target Customer (Name)", placeholder="e.g., John Doe")

    st.header("2. Company Data")
    
    # URL Inputs [cite: 44, 48]
    company_url = st.text_input("Target Company URL", placeholder="https://www.target-company.com")
    competitor_urls = st.text_area("Competitor URLs (one per line)", placeholder="https://www.competitor1.com\nhttps://www.competitor2.com")

    # Optional Upload [cite: 51]
    uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=['txt', 'pdf', 'md'])

    # Submit Button
    submitted = st.form_submit_button("Generate Insights")

if submitted:
    # This block will run when the button is clicked
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: GOOGLE_API_KEY not found in .env file.")
    elif not product_name or not company_url:
        st.warning("Please fill in the Product Name and Target Company URL.")
    else:
        st.success(f"Inputs received! Ready to analyze {company_url} for {product_name}.")
        # logic for scraping and AI generation will go here later
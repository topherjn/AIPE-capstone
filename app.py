import streamlit as st
import os
from dotenv import load_dotenv
from scraper import scrape_url
from agent import generate_sales_insights  # <--- IMPORT THE AGENT

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Sales Agent", page_icon="💼", layout="wide")

st.title("💼 Sales Assistant Agent")
st.markdown("Generate account insights, competitor analysis, and strategy summaries.")

# Sidebar for API Key (optional security measure) or just informational
with st.sidebar:
    st.info("System Status: Ready")
    if os.getenv("GOOGLE_API_KEY"):
        st.success("API Key Detected")
    else:
        st.error("Missing API Key")

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
    
    st.header("2. Competitor Analysis")
    competitor_urls = st.text_area("Competitor URLs (one per line)", placeholder="https://www.competitor1.com")

    submitted = st.form_submit_button("Generate Insights")

if submitted:
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: GOOGLE_API_KEY not found in .env file.")
    elif not product_name or not company_url:
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
            
            st.write("Processing data with Gemini Pro...")
            
            # 3. Call AI Agent
            insights = generate_sales_insights(
                product_name, 
                product_category, 
                value_proposition, 
                target_customer, 
                company_data, 
                competitor_data_list
            )
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # 4. Display Result
        st.divider()
        st.markdown(insights)
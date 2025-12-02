import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Sales Agent Prototype Check")

if os.getenv("GOOGLE_API_KEY"):
    st.success("API Key found!")
else:
    st.error("API Key not found. Check your .env file.")
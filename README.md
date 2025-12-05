# Sales Agent Prototype (CAP 931) - V2.0 "AI Workbench"

This repository contains a functional prototype of a Sales Assistant Agent. Originally built on **Google Gemini**, Version 2.0 has been upgraded to a "Hybrid" architecture that supports **Google Gemini**, **GitHub Models (GPT-4o)**, and **Hugging Face**.

The application helps sales representatives generate "one-pager" insights by scraping target company websites, analyzing competitors, and parsing product manuals.

**[Live Demo Available Here](https://aipe-capstone.onrender.com/)**
*(Note: Hosted on Render Free Tier; please allow 60 seconds for the instance to spin up from sleep.)*

## 🚀 V2.0 Key Features
* **Multi-Model Intelligence:**
    * **Google:** Native integration (Gemini 1.5 Flash / Pro).
    * **GitHub Models:** Free-tier access to **GPT-4o** via Azure/OpenAI compatibility.
    * **Hugging Face:** Serverless inference for Open Source models (Llama 3, Mistral).
* **Smart Web Scraping:** Uses `markdownify` to convert HTML to Markdown, preserving hyperlinks to ensure the AI can generate valid **Article Links** and citations.
* **Refinement Chain (Experiment D):** Optional "Self-Correction" mode where a second AI pass acts as a Senior Editor to verify facts and improve formatting.
* **Prompt Engineering UI:** "Power User" sidebar allows real-time editing of the System Prompt to test different personas and instructions.
* **PDF Analysis:** Parsing engine (`pypdf`) to ingest uploaded product manuals or strategy decks.

## 🛠️ Technical Setup

### Prerequisites
* Python 3.10+
* API Keys (see below)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/AIPE-capstone.git](https://github.com/your-username/AIPE-capstone.git)
    cd AIPE-capstone
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory. You only need the keys for the providers you intend to use.
    ```text
    # Google Gemini (Native)
    GOOGLE_API_KEY=your_google_key_here

    # GitHub Models (Free GPT-4o access)
    # Get token here: [https://github.com/settings/tokens](https://github.com/settings/tokens)
    GITHUB_TOKEN=ghp_your_personal_access_token

    # Hugging Face (Open Source Models)
    # Get token here: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
    HF_TOKEN=hf_your_huggingface_token
    ```

### Running the App
To start the Streamlit interface locally:

```bash
streamlit run app.py

# Sales Agent Prototype (CAP 931)

This repository contains a functional prototype of a Sales Assistant Agent. Originally built on **Google Gemini**, Version 2.0 has been upgraded to a "Hybrid" architecture that supports **Google Gemini**, **GitHub Models (GPT-4o)**, and **Hugging Face**.

The application helps sales representatives generate "one-pager" insights by scraping target company websites, analyzing competitors, and parsing product manuals.

**[Live Demo Available Here](https://aipe-capstone.onrender.com/)**
*(Note: Hosted on Render Free Tier; please allow 60 seconds for the instance to spin up from sleep.)*

## 🚀 Key Features
* **Automated Web Scraping:** Extracts text from target company and competitor URLs.
* **PDF Analysis:** Optional upload for product manuals or strategy decks.
* **AI-Powered Insights:** Uses Large Language Models (LLM) to synthesize strategy, leadership info, and sales pitches.
* **Dynamic Model Selection:** Currently running on `gemini-flash-latest` for high speed and lower latency.
* **Source Citation:** Provides links to valid sources found during the scrape.

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

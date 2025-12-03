# Sales Agent Prototype (CAP 931)

This repository contains a functional prototype of a Sales Assistant Agent powered by **Google Gemini 1.5 Flash**. The application helps sales representatives generate "one-pager" insights by scraping target company websites, analyzing competitors, and parsing product manuals.

**[Live Demo Available Here](https://aipe-capstone.onrender.com/)**

## 🚀 Key Features
* **Automated Web Scraping:** Extracts text from target company and competitor URLs.
* **PDF Analysis:** Optional upload for product manuals or strategy decks.
* **AI-Powered Insights:** Uses Large Language Models (LLM) to synthesize strategy, leadership info, and sales pitches.
* **Dynamic Model Selection:** Currently running on `gemini-1.5-flash-latest` for high speed and lower latency.
* **Source Citation:** Provides links to valid sources found during the scrape.

## 🛠️ Technical Setup

### Prerequisites
* Python 3.10+
* Google Gemini API Key

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
    Create a `.env` file in the root directory:
    ```text
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

### Running the App
To start the Streamlit interface locally:

```bash
streamlit run app.py
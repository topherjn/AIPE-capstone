import pypdf

def extract_text_from_pdf(uploaded_file):
    """
    Reads a PDF file object from Streamlit and returns the text.
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Limit text to ~10,000 chars to avoid blowing up the context window
        return text[:10000]
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
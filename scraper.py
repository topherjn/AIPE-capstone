import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    """
    Fetches the content of a URL and returns the visible text.
    """
    try:
        # Fake a browser visit to avoid 403 Forbidden errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()    

        text = soup.get_text(separator=' ')
        
        lines = (line.strip() for line in text.splitlines())
        clean_text = '\n'.join(chunk for chunk in lines if chunk)
        
        return clean_text[:8000]
        
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
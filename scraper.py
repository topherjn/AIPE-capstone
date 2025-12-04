import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from markdownify import markdownify as md

def scrape_url(url):
    """
    Fetches URL and converts HTML to Markdown to preserve links.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Clean up junk
        for script in soup(["script", "style", "nav", "footer", "iframe", "noscript"]):
            script.decompose()
            
        # 2. Fix Relative Links (Critical for "Article Links" to work)
        # Changes <a href="/about"> to <a href="https://target.com/about">
        for a in soup.find_all('a', href=True):
            a['href'] = urljoin(url, a['href'])

        # 3. Convert to Markdown (Preserves Links)
        # We strip images to save tokens, but keep links (a)
        clean_html = str(soup)
        markdown_text = md(clean_html, strip=['img'])
        
        # 4. Clean up excessive whitespace
        lines = [line.strip() for line in markdown_text.splitlines() if line.strip()]
        return '\n'.join(lines)[:12000] # Increased limit slightly for links
        
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
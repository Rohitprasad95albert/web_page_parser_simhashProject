import sys
import requests
import bs4
from urllib.parse import urljoin

def fetch_page(url):
    print("fetching page.......")
    headers = {
    "User-Agent": "Mozilla/5.0"
}
    try:
        response = requests.get(url, timeout=30, headers=headers)
        #print(f"Response status code: {response.status_code}")
        #print(f"Response headers: {response.headers}")
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    else:

        status_code = response.status_code
        if status_code == 200:
            print("URL is valid")
        else:
            print(f"URL returned status code: {status_code}")
            return
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    
    return soup


def Page_title(soup):
    if soup.title is not None:
        return soup.title.get_text()
    else:
        return "No title found"
    
def Page_Body(soup):
    if soup.body is not None:
        return soup.body.get_text()
    else:
        return "No body found"
    
def page_links(soup,url):
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is None or href.startswith('#'):
            continue 
        if href.startswith('http'):
            print(href)           
        if href.startswith('/'):
            href = urljoin(url, href)
            print(href)
def main():
    if len(sys.argv) != 2:
        print("Please provide a URL as a command-line argument.")
        sys.exit(1)

    url = sys.argv[1]
    
    print(f"URL received: {url}")

    soup = fetch_page(url)
    if soup:
        print("Page fetched successfully.")
        #print(soup.prettify())
        print()
        print("Page title:", Page_title(soup))
        print("Page body:", Page_Body(soup))
        print("Page links:")
        page_links(soup,url)

if __name__ == "__main__":    
    main()
import re
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
        response= requests.get(url, timeout=30, headers=headers)
        #response2= requests.get(url2, timeout=30, headers=headers)

        #print(f"Response status code: {response.status_code}")
        #print(f"Response headers: {response.headers}")
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    else:

        status_code = response.status_code
        #status_code2 = response2.status_code
        if status_code == 200:
            print(" URL are valid")
        else:
            print(f"URL returned status code: {status_code}")
            #print(f"URL2 returned status code: {status_code2}")
            return
    
    #soup1 = bs4.BeautifulSoup(response1.text, 'html.parser')
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    
    return soup

def countword_frequency(soup):
    soup_text = soup.get_text().lower()
    words = re.findall(r'[a-z0-9]+', soup_text)
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    return word_freq


def word_hash(word):
    p = 53
    hash_value = 0
    
    for i in range(len(word)):
        hash_value += ord(word[i]) * (p ** i)       # ord() converts a character to its ASCII value

    return hash_value % (2**64)



def compute_Simhash(word_freq):
    V = [0] * 64

    for word in word_freq:
        h = word_hash(word)
        weight = word_freq[word]

        for i in range(64):
            if ((h >> i) & 1) == 1:
                V[i] += weight
            else:
                V[i] -= weight

    simhash = 0

    for i in range(64):
        if V[i] > 0:
            simhash += (2 ** i)

    return simhash  


def common_bits(simhash1, simhash2):
    x = simhash1 ^ simhash2
    count = 0
    while x:
        count += 1
        x &= x - 1
    return 64 - count


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
    if len(sys.argv) != 3:
        print("Please provide two URLs as command-line arguments.")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]
    
    print(f"URL1 received: {url1}")
    print(f"URL2 received: {url2}")

    soup1 = fetch_page(url1)
    soup2 = fetch_page(url2)
    if soup1 and soup2:
        print("Pages fetched successfully.")
        #print(soup.prettify())
        print()
        print("Page title of url1:", Page_title(soup1))
        print("Page body of url1:", Page_Body(soup1))
        print("Page links of url1:")
        page_links(soup1,url1)
        word_freq1= countword_frequency(soup1)
        word_freq2 = countword_frequency(soup2)
       # word_hash1 = word_hash(word_freq1)
        #word_hash2 = word_hash(word_freq2)
        #print("Word hash value for the first page:", word_hash1)
        #print("Word hash value for the second page:", word_hash2)
        simhash1= compute_Simhash(word_freq1)
        #print("Simhash value for the first page:", bin(simhash1)[2:]) # format the simhash value as a binary string and remove the '0b' prefix
        simhash2 = compute_Simhash(word_freq2)
        #print("Simhash value for the second page:", bin(simhash2)[2:])
        print("Simhash value for the first page:", format(simhash1, '064b'))   # format the simhash value as a 64-bit binary string
        print("Simhash value for the second page:", format(simhash2, '064b'))
        simhash_common_bit = common_bits(simhash1, simhash2)
        print("Number of common bits:", simhash_common_bit)


if __name__ == "__main__":    
    main()
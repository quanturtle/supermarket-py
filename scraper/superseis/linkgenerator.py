import requests
from bs4 import BeautifulSoup

def main():
    url = "https://www.superseis.com.py/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    all_a = soup.find_all("a")
    seen_links = set()

    for link in all_a:
        href = link.get("href")
        if href is not None and 'category' in href and href not in seen_links:
            seen_links.add(href)
            url = link.get("href")
            resp = requests.post('http://localhost:8000/api/link/', data={'supermarket': 1, 'url': url})
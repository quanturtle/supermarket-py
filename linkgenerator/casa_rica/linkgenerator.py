import requests
from bs4 import BeautifulSoup

def main():
    base_url = "https://casarica.com.py/"
    response = requests.get(base_url)

    soup = BeautifulSoup(response.text, "html.parser")

    all_a = soup.find_all("a")
    seen_links = set()

    for link in all_a:
        href = link.get("href")
        if href is not None and href not in seen_links and 'catalogo' in href:
            seen_links.add(href)
            href = base_url + href
            resp = requests.post('http://localhost:8000/api/link/', data={'supermarket': 2, 'url': href})

main()
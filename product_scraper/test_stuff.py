import requests
from product_scraper.spiders.supermarket import Supermarket

def main():
    resp = requests.get(f'http://localhost:8000/api/link/?supermarket={Supermarket.CASA_RICA}')
    resp = resp.json()

    for elem in resp:
        print(elem['url'])

main()
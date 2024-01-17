from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

def scrape_all_pages_links(url_home):
    all_links_img_urls = []
    page = requests.get(url_home)
    soup = BeautifulSoup(page.text, "html.parser")
    page_number = soup.find_all('li', class_='current')
    x = int(page_number[0].text.split()[-1])
    if x > 1:
        for i in range(1, x+1):
            page_url = f"{url_home}/page-{i}.html"
            page = requests.get(page_url)
            soup = BeautifulSoup(page.text, "html.parser")
            links = soup.find_all('img')
            links_img_urls = [urljoin(url_home, link['src']) for link in links]
            all_links_img_urls.extend(links_img_urls)
        return all_links_img_urls

url_home = "https://books.toscrape.com"
image_links = scrape_all_pages_links(url_home)
print(image_links)

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

def scrape_all_pages_links(url_home): # fonction pour récupérer les liens des images
    all_links_img_urls = []
    page = requests.get(url_home)
    soup = BeautifulSoup(page.text, "html.parser")
    page_number = soup.find_all('li', class_='current')
    x = int(page_number[0].text.split()[-1])
    if x > 1:
        for i in range(1, x+1):
            page_url = f"{url_home}/catalogue/page-{i}.html"
            page = requests.get(page_url)
            soup = BeautifulSoup(page.text, "html.parser")
            links = soup.find_all('img')
            links_img_urls = [urljoin(url_home, link['src'].replace('../', '')) for link in links] # urljoin - pour joindre l'url de la page et l'url de l'image
            all_links_img_urls.extend(links_img_urls)
    return all_links_img_urls

url_home = "https://books.toscrape.com"
image_links = scrape_all_pages_links(url_home) # Lance la fonction pour récupérer les liens des images stockés dans une liste image_links
# print(image_links)
# Ou fo écrire les images  
dossier_pour_images = r"D:\All OpenClassRooms projects\P2 - Books to Scrape\P2---Books-to-Scrape\phase 4"

def download_images(image_links, dossier_pour_images): # on envoie les liens de la liste ici pour télécharger les images
    for url in image_links:
        img_data = requests.get(url).content
        filename = dossier_pour_images + '/' + url.split('/')[-1] # pas trop compris mais apparemment c'est indispensable pour écrire les fichiers, marche pas avec juste "url"
        with open(filename, 'wb') as handler: # 'wb' - write binary - pour écrire les fichiers, fait partie de requests
            handler.write(img_data)


# lance la fonction pour télécharger les images
download_images(image_links, dossier_pour_images)
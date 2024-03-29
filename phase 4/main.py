from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from urllib.parse import urljoin
import os
# import des librairies nécéssaires



url_home = "https://books.toscrape.com" # url du site à scraper 



def get_cat_links(): # fonction pour récupérer les liens des catégories
    page_de_site_home = requests.get(url_home)
    soup_home = BeautifulSoup(page_de_site_home.text, "html.parser")

    ttes_categories = soup_home.find('ul', class_="nav nav-list")
    links = ttes_categories.find_all('a')
    links_cat_urls = [urljoin(page_de_site_home.url, link['href']) for link in links]
    
    return links_cat_urls



def scrape_category_links(category_url): # fonction pour récupérer les liens des livres de la catégorie
    all_links_book_urls = []
    url_de_base = category_url.split('/index.html')[0]
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, "html.parser")
    page_number = soup.find_all('li', class_='current') # cherche le numéro de la page
    if not page_number: # si pas de numéro de page, alors la page est la page initial (avec index.html à la fin)
        links = soup.find_all('h3')  # cherche les links dans les balises h3
        links_book_urls = [urljoin(category_url, link.find('a')['href']) for link in links]    # cherche les liens des livres dans les balises h3
        all_links_book_urls.extend(links_book_urls) #   ajoute les liens des livres dans la liste all_links_book_urls
    else: # si il y a un numéro de page
        x = int(page_number[0].text.split()[-1]) # récupère le numéro de la page
        if x > 1:  # si le numéro de la page est supérieur à 1
            for i in range(1, x+1):     # cycle pour parcourir les pages de la catégorie
                page_url = f"{url_de_base}/page-{i}.html" # cycle pour parcourir les pages de la catégorie
                page = requests.get(page_url) # ici category_url est la page de la catégorie à scraper après la condition ci-dessus
                soup = BeautifulSoup(page.text, "html.parser")
                links = soup.find_all('h3')  # cherche les links dans les balises h3
                links_book_urls = [urljoin(page_url, link.find('a')['href']) for link in links]    # cherche les liens des livres dans les balises h3
                all_links_book_urls.extend(links_book_urls) #   ajoute les liens des livres dans la liste all_links_book_urls
    return all_links_book_urls # retourne la liste all_links_book_urls

links_cat_urls = get_cat_links() # récupère les liens des catégories

# all_book_urls = {}  # créer une liste vide pour y mettre les liens des livres


# 2ème partie du code pour scraper les données des livres
titres = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
df = pd.DataFrame(columns=titres) # créer un dataframe vide avec les titres des colonnes


def load_book_data(link): # fonction pour scraper les données d'une livre
    page_de_site = requests.get(link) # récupère la page du livre dans le lien link qui est le résultat de la fonction scrape_category_links
    soup = BeautifulSoup(page_de_site.text, "html.parser")

    product_page_url = page_de_site.url
    universal_product_code = soup.find("td").string
    title = soup.find("h1").string
    price_including_tax = soup.find(string='Price (incl. tax)').find_next('td').string.replace('Â', '')
    price_excluding_tax = soup.find(string='Price (excl. tax)').find_next('td').string.replace('Â', '')
    number_available = soup.find(string='Availability').find_next('td').string
    product_description_element = soup.find(string='Product Description')
    if product_description_element is None:
        product_description = "Y'en a pas"
    else:
        product_description = product_description_element.find_next('p').string
    category = soup.find_all('a')[3].string
    review_rating = soup.find_all('p')[2]['class'][1]
    image_url_relative = soup.find('img')['src']
    image_url = urljoin(page_de_site.url, image_url_relative) #  VOIR COMMENT TELECHARGER LES IMAGES ICI!!!!

        # fo faire en dictionnaire et pas en liste pour pouvoir utiliser la fonction writerow!!!!
    book_data = {
        "product_page_url": product_page_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }
    return book_data #

chemin_dossier = input("Entrez le chemin du dossier où vous voulez enregistrer les fichiers .csv et les images:") # demande à l'utilisateur le chemin du dossier où il veut enregistrer les fichiers .csv et les images

for category_url in links_cat_urls: # pour chaque url de catégorie dans la liste links_cat_urls (récupérée avec la fonction get_cat_links)
    all_links_cat_urls = scrape_category_links(category_url)  # la fonction scrape_category_links retourne la liste des liens des livres de la catégorie
    for link in all_links_cat_urls:
        book_data = load_book_data(link)
        book_data_df = pd.DataFrame([book_data]) # convertir en df car append ne marche pas avec les dictionnaires
        df = pd.concat([df, book_data_df], ignore_index=True)  # concatène les df dans df
        for image_url in book_data_df['image_url']:
            img_data = requests.get(image_url).content
            category_name = category_url.split('/')[-2]
            dossier_pour_images = os.path.join(chemin_dossier, f"images_{category_name}")
            os.makedirs(dossier_pour_images, exist_ok=True)  # cela crée le dossier pour les images si il n'existe pas déjà, sinon ne fait rien
            filename = os.path.join(dossier_pour_images, image_url.split('/')[-1])
            with open(filename, 'wb') as handler: # 'wb' - write binary - pour écrire les fichiers, fait partie de requests
                handler.write(img_data) # écrit les fichiers images dans le dossier images
    category_name = category_url.split('/')[-2] # pour rajouter le nom de la catégorie dans le nom du ficD:\All OpenClassRooms projects\P2 - Books to Scrape\P2---Books-to-Scrape\phase 4hier .csv
    df.to_csv(os.path.join(chemin_dossier, f"scrape_phase_4_{category_name}.csv"), index=False) # écrit les fichiers .csv dans le dossier qu'on a saisie au début
    
    df = pd.DataFrame(columns=titres) # quand la df est écrit dans le fichier .csv cela vide la df de nouveau pour la prochaine catégorieD:\All OpenClassRooms projects\P2 - Books to Scrape\P2---Books-to-Scrape\phase 4
    # push après la suppression sur github
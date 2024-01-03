from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin
import pandas as pd

# import des librairies nécéssaires




page_de_site= requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# récupération de la page web et stockage dans une variable
soup= BeautifulSoup(page_de_site.text, "html.parser")
# utilisation de BeautifulSoup pour parser la page web

# file = open("scrape_phase_1.csv", "w")
# # ouverture du fichier csv pour enregistrement des données
# writer = csv.writer(file)
# # writer pour écrire dans le fichier csv
# writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"])


def load_only_1_book_data(data):
    # création d'une liste vide pour stocker les données
    with open ('scrape_phase_1.csv', 'w') as csv_file:
        titres = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csv_file, fieldnames=titres)
        writer.writeheader()
        writer.writerow(data)

    
product_page_url = page_de_site.url
# url de la page actuelle
universal_product_code = soup.find("td").text
# récupération du code produit
title = soup.find("h1").text
# récupération du titre
price_including_tax = soup.find(text='Price (incl. tax)').find_next('td').text.replace('Â', '')
# price_including_tax = price_including_tax_A.replace('Â', '')
# récupération du prix ttc sans le symbole Â
price_excluding_tax = soup.find(text='Price (excl. tax)').find_next('td').text.replace('Â', '')
# price_excluding_tax = price_excluding_tax_A.replace('Â', '')
# récupération du prix ht sans le symbole Â
number_available = soup.find(text='Availability').find_next('td').text
# récupération du nombre d'articles disponibles
product_description = soup.find(text='Product Description').find_next('p').text
# récupération de la description du produit
category = soup.find_all('a')[3].text
# récupération de la catégorie du produit ou [3] numéro de link dans la liste des links de la page. Cela a été DURE!!!!!!
review_rating = soup.find_all('p')[2]['class'][1]
# récupération de la note. ou [2] numéro de paragraphe - 3 par. de la page. ['class'] - attribut de la balise - [1] numéro de la balise à choisir.
image_url_relative = soup.find('img')['src']
image_url = urljoin(page_de_site.url, image_url_relative)
# récupération de l'url de l'image ('img') ou ['src'] - attribut de la balise; urljoin - pour joindre l'url de la page et l'url de l'image

data = {
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
# fo faire en dictionnaire et pas en liste pour pouvoir utiliser la fonction writerow!!!!


print(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)

load_only_1_book_data(data)  # lancer la fonction pour enregistrer les données dans le fichier csv

# with open('scrape_phase_1.csv', 'w') as csv_file:
#     writer= csv.writer(csv_file, delimiter=',')
#     writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"])
#     for (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url) in zip(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
#         writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    
# writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
# file.close()


# trouver tous les liens des catégories principales
page_de_site_home= requests.get("https://books.toscrape.com")
# récupération de la page HOME
soup= BeautifulSoup(page_de_site_home.text, "html.parser")


# ttes_categories = soup.find('div', class_="side_categories").find_all('a')
# # Extraire les liens des catégories principales
# links = [ttes_categories['href'] for categorie in ttes_categories]
# print(links)

ttes_categories = soup.find('ul', class_="nav nav-list")
if ttes_categories:
    links = ttes_categories.find_all('a')
    links_cat_urls = [urljoin(page_de_site_home.url, link['href']) for link in links]
    print(links_cat_urls)
else:
    print("No links found.")

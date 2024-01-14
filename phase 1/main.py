from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# import des librairies nécéssaires



def load_only_1_book_data(data):
    with open (r'D:\All OpenClassRooms projects\P2 - Books to Scrape\P2---Books-to-Scrape\phase 1\scrape_phase_1.csv', 'a', newline='') as csv_file:
        titres = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csv_file, fieldnames=titres)
        # write header seulement si le fichier est vide, sinon il va écrire le header à chaque fois
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)
# écriture de la fonction pour enregistrer les données dans le fichier csv

page_de_site= requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# récupération de la page web et stockage dans une variable
soup= BeautifulSoup(page_de_site.text, "html.parser")
# utilisation de BeautifulSoup pour parser la page web
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
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
# import des librairies nécéssaires



# Choisissez n'importe quelle catégorie sur le site de Books to Scrape. Écrivez un
# script Python qui consulte la page de la catégorie choisie, et extrait l'URL de la
# page Produit de chaque livre appartenant à cette catégorie.
# Combinez cela avec le travail que vous avez déjà effectué dans la phase 1 afin
# d'extraire les données produit de tous les livres de la catégorie choisie, puis écrivez
# les données dans un seul fichier CSV.
# Remarque : certaines pages de catégorie comptent plus de 20 livres, qui sont
# donc répartis sur différentes pages (« pagination »). Votre application doit être
# capable de parcourir automatiquement les multiples pages si présentes


# On choisit la catégorie "Mystery" pour tester le code

demande_chemin_dossier = input("Entrez le chemin du dossier où vous voulez enregistrer le fichier .csv") # demande à l'utilisateur le chemin du dossier où il veut enregistrer les fichiers .csv et les images
chemin_dossier = os.path.join(demande_chemin_dossier, "mystery_3.csv") # crée le chemin du fichier .csv

def scrape_category_links(category_url):
    all_links_book_urls = []
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, "html.parser")
    page_number = soup.find_all('li', class_='current')
    x = int(page_number[0].text.split()[-1])
    for i in range(1, x+1):
        category_url = f"https://books.toscrape.com/catalogue/category/books/mystery_3/page-{i}.html" # cycle pour parcourir les pages de la catégorie
        page = requests.get(category_url)
        soup = BeautifulSoup(page.text, "html.parser")
        links = soup.find_all('h3')  # cherche les links dans les balises h3
        links_book_urls = [urljoin(category_url, link.find('a')['href']) for link in links]
        all_links_book_urls.extend(links_book_urls)
    return all_links_book_urls
category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html"
result = scrape_category_links(category_url)
# print(result)

titres = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
df = pd.DataFrame(columns=titres)


def load_book_data(link):
    page_de_site = requests.get(link)
    soup = BeautifulSoup(page_de_site.text, "html.parser")

    product_page_url = page_de_site.url
    universal_product_code = soup.find("td").string
    title = soup.find("h1").string
    price_including_tax = soup.find(string='Price (incl. tax)').find_next('td').string.replace('Â', '')
    price_excluding_tax = soup.find(string='Price (excl. tax)').find_next('td').string.replace('Â', '')
    number_available = soup.find(string='Availability').find_next('td').string
    product_description = soup.find(string='Product Description').find_next('p').string
    category = soup.find_all('a')[3].string
    review_rating = soup.find_all('p')[2]['class'][1]
    image_url_relative = soup.find('img')['src']
    image_url = urljoin(page_de_site.url, image_url_relative)

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
    return book_data

for link in result:
    book_data = load_book_data(link)
    book_data_df = pd.DataFrame([book_data])  # convertir en df car append ne marche pas avec les dictionnaires
    df = pd.concat([df, book_data_df], ignore_index=True)

df.to_csv(chemin_dossier, index=False)
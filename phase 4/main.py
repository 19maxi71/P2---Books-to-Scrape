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
# import des librairies nécéssaires


def load_only_1_book_data(data):
    with open(r'D:\All OpenClassRooms projects\P2 - Books to Scrape\P2 - phase 1\scrape_phase_1.csv', 'a', newline='') as csv_file:
        titres = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csv_file, fieldnames=titres)
        # write header seulement si le fichier est vide, sinon il va écrire le header à chaque fois
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)
# écriture de la fonction pour enregistrer les données dans le fichier csv

page_de_site = requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# récupération de la page web et stockage dans une variable
soup = BeautifulSoup(page_de_site.text, "html.parser")
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

load_only_1_book_data(data) # lancer la fonction pour enregistrer les données dans le fichier csv




# # Choisissez n'importe quelle catégorie sur le site de Books to Scrape. Écrivez un
# # script Python qui consulte la page de la catégorie choisie, et extrait l'URL de la
# # page Produit de chaque livre appartenant à cette catégorie.
# # Combinez cela avec le travail que vous avez déjà effectué dans la phase 1 afin
# # d'extraire les données produit de tous les livres de la catégorie choisie, puis écrivez
# # les données dans un seul fichier CSV.
# # Remarque : certaines pages de catégorie comptent plus de 20 livres, qui sont
# # donc répartis sur différentes pages (« pagination »). Votre application doit être
# # capable de parcourir automatiquement les multiples pages si présentes

# def scrape_category_links(category_url):
#     all_links_book_urls = []
#     page = requests.get(category_url)
#     soup = BeautifulSoup(page.text, "html.parser")
#     page_number = soup.find_all('li', class_='current')
#     x = int(page_number[0].text.split()[-1])
#     for i in range(1, x+1):
#         category_url = f"https://books.toscrape.com/catalogue/category/books/mystery_3/page-{i}.html" # cycle pour parcourir les pages de la catégorie
def scrape_category_links(category_url, category_name):
    all_links_book_urls = []
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, "html.parser")
    
    if soup.find('li', class_='current'):
        page_number = soup.find_all('li', class_='current')
        x = int(page_number[0].text.split()[-1])
        for i in range(1, x + 1):
            category_url = f"{url_home}/catalogue/category/books/{category_name}/page-{i}.html"
            page = requests.get(category_url)
            soup = BeautifulSoup(page.text, "html.parser")
            links = soup.find_all('h3')
            links_book_urls = [urljoin(category_url, link.find('a')['href']) for link in links]
            all_links_book_urls.extend(links_book_urls)
    else:
        category_url = f"{url_home}/catalogue/category/books/{category_name}/index.html"
        page = requests.get(category_url)
        soup = BeautifulSoup(page.text, "html.parser")
        links = soup.find_all('h3')
        links_book_urls = [urljoin(category_url, link.find('a')['href']) for link in links]
        all_links_book_urls.extend(links_book_urls)
    return all_links_book_urls

url_home = "https://books.toscrape.com"
page_de_site_home = requests.get(url_home)
soup_home = BeautifulSoup(page_de_site_home.text, "html.parser")

ttes_categories = soup_home.find('ul', class_="nav nav-list")
links = ttes_categories.find_all('a')
links_cat_urls = [urljoin(page_de_site_home.url, link['href']) for link in links]

category_names = [url.split('/')[-2] for url in links_cat_urls]

all_results = []
for category_name in category_names[2:]:
    category_url = f"{url_home}/catalogue/category/books/{category_name}/page-1.html"
    result = scrape_category_links(category_url, category_name)
    all_results.extend(result)

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

    product_description_tag = soup.find(string='Product Description')
    product_description = product_description_tag.find_next('p').string if product_description_tag else None

    category = soup.find_all('a')[3].string
    review_rating = soup.find_all('p')[2]['class'][1]
    image_url_relative = soup.find('img')['src']
    image_url = urljoin(page_de_site.url, image_url_relative)

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

for link in all_results:
    book_data = load_book_data(link)
    book_data_df = pd.DataFrame([book_data])  # convertir en df car append ne marche pas avec les dictionnaires
    df = pd.concat([df, book_data_df], ignore_index=True)

df.to_csv("scrape_phase_2.csv", index=False)
from bs4 import BeautifulSoup
import requests
# import les librairies nécéssaires
page_de_site= requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# récupération de la page web et stockage dans une variable
soup= BeautifulSoup(page_de_site.text, "html.parser")
# utilisation de BeautifulSoup pour parser la page web
product_page_url = page_de_site.url
# url de la page actuelle
print(product_page_url)
# -*-coding:Utf-8 -*

import os # On importe le module os 
import requests # module qui permet d'interagir avec une url
import time  # module permettent de rajouter delai dans l'exécution du code pour éviter de faire saturer le site en requêtes

import fonctions as f

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web


# Initialisatin du fichier csv des livres d'une catégorie avec la ligne des entêtes
with open("f_book.csv", "w") as fichier_book:
    fichier_book.write("""product_page_url, 
                        universal_ product_code (upc), 
                        title, 
                        price_including_tax, 
                        price_excluding_tax, 
                        number_available, 
                        product_description, 
                        category, 
                        review_rating""")




# URL d'une page des détails d'un livre
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Gestion des exception sur la requête sur l'url:
validation_url, response_book = f.validation_url(url)

# Préparation pour l'analyse avec analyseur lxml
soup_book = BeautifulSoup(response_book.text, 'lxml')

# On recherche le titre
title = soup_book.find("div", {"class" : "col-sm-6 product_main"}).find("h1")

# On recherche la catégorie
category = soup_book.find("ul", {"class" : "breadcrumb"}).findAll("a")[2]

# On recherche le résumé du livre
product_description = soup_book.find("article", {"class" : "product_page"}).findAll("p")[3]

# Recherche des données Product Information
Prod_Info = soup_book.find("table", {"class" : "table table-striped"}).findAll("tr")

# Pour chaque ligne de extract on crée une clé et une valeur dans Book_dico
info_liste = []
for tr in Prod_Info:
    info_liste.append(tr.find("td").text)


with open("f_book.csv", "w") as fichier_book:
    fichier_book.write(url + ',' + 
    info_liste[0] + ',' +
    title.text + ',' +
    info_liste[3].replace('Â£', '') + ',' +
    info_liste[2].replace('Â£', '') + ',' +
    info_liste[4] + ',' +
    product_description.text + ',' +
    category.text + ',' +
    info_liste[6])


print(info_liste)





os.system("pause") # met en pause pour éviter la fermeture de la fenêtre d'excécution
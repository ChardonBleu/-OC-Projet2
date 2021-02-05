# -*-coding:Utf-8 -*

import os # On importe le module os 
import requests # module qui permet d'interagir avec une url
import time  # module permettent de rajouter delai dans l'exécution du code pour éviter de faire saturer le site en requêtes

import fonctions as f

import bs4
from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web


#  création du fichier csv pour une catégorie
cat = 'poetry'
f.Entete_csv_cat(cat + '.csv') # Ecriture des entêtes dans le ficheir csv

# URL de la page d'acceuil catégorie poetry
url_cat = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html
"
# http://books.toscrape.com/catalogue/category/books/mystery_3/index.html
# http://books.toscrape.com/catalogue/category/books/poetry_23/index.html
# http://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html

# Initialisation de la lsite des url des livres pour cette catégorie
liste_url_cat = []
# Gestion des esceptions sur la requete
valid_url, response = f.validation_url(url_cat)
if valid_url:
    # On prépare pour analyse 
    soup_cat = BeautifulSoup(response.text, "lxml") # Préparation pour l'analyse avec analyseur lxml

    # Recherche s'il y a plusieurs pages
    Nb_page = soup_cat.find("li", {"class" : "current"})
    # Si il y a plusieurs pages, un élément a été trouvé et alors nb_page est du type bs4.element.Tag
    if isinstance(Nb_page, bs4.element.Tag):
        # On récupère le nombre de pages:
        Nb_page = int(Nb_page.text.strip()[-1])        
        #Pour chaque page on récupère les url des livres dans une liste
        for i in range(1,Nb_page+1):
            # On met en forme l'url de la page i:
            url_cat_p = url_cat.replace("index.html", '') + "page-" + str(i) + ".html"
            print(url_cat_p)
    else: # Si Nb_page n'est pas du type bs4.elemnt.Tag, c'est qu'il n'y a qu'une page
        print(url_cat)
        



# URL d'une page des détails d'un livre
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

f.data_one_book(url, cat) # Ecriture des données pour ce livre dans le scv de la catégorie
time.sleep(1)


os.system("pause") # met en pause pour éviter la fermeture de la fenêtre d'excécution
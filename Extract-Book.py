# -*-coding:Utf-8 -*

import os # On importe le module os 
import requests # module qui permet d'interagir avec une url
import time  # module permettent de rajouter delai dans l'exécution du code pour éviter de faire saturer le site en requêtes

import fonctions as f

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web


#  création du fichier csv pour une catégorie
cat = 'poetry'
f.Entete_csv_cat(cat + '.csv') # Ecriture des entêtes dans le ficheir csv

# URL d'une page des détails d'un livre
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

f.data_one_book(url, cat) # Ecriture des données pour ce livre dans le scv de la catégorie


os.system("pause") # met en pause pour éviter la fermeture de la fenêtre d'excécution
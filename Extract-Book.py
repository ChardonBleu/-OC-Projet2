# -*-coding:Utf-8 -*

import os # On importe le module os 
import time  # module permettent de rajouter delai dans l'exécution du code pour éviter de faire saturer le site en requêtes

import fonctions as f

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web


time1 = time.process_time()
# Construction de la liste des catégories à partir de la page accueuil du site
url_site = "http://books.toscrape.com/index.html"

#Initialisation de la liste des url
liste_url_cat = []
# Gestion des exceptions sur la requete
valid_url, response = f.validation_url(url_site)
if valid_url:
    #On prépare pour analyse 
    soup_index = BeautifulSoup(response.text, "lxml") # Préparation pour l'analyse avec analyseur lxml
    liste_li = soup_index.find('ul', {'class' : "nav nav-list"}).find('ul').find_all('li')
    # On boucle sur toutes les catégories
    for li in liste_li:
        a = li.find('a')
        cat = a.get_text().strip()
        url_cat = 'http://books.toscrape.com/' + a['href']
        print(cat)
        #  création du fichier csv pour une catégorie
        f.Entete_csv_cat(cat + '.csv') # Ecriture des entêtes dans le ficheir csv
        
        # Initialisation de la lsite des url des livres pour cette catégorie
        url_book_cat = []
        valid_url, response = f.validation_url(url_cat)
        if valid_url:
            #On prépare pour analyse 
            soup_cat = BeautifulSoup(response.text, "lxml") # Préparation pour l'analyse avec analyseur lxml
            # Recherche du nombre de pages:
            Nombre_pages = f.Nombre_page_categorie(soup_cat)

            if Nombre_pages > 1:
                #Pour chaque page on récupère les url des livres dans une liste
                for i in range(1, Nombre_pages + 1):
                    # On met en forme l'url de la page i:
                    url_cat_p = url_cat.replace("index.html", '') + "page-" + str(i) + ".html"
                    valid_url_p, response = f.validation_url(url_cat_p)
                    if valid_url:
                        # On prépare pour analyse 
                        soup_cat = BeautifulSoup(response.text, "lxml") # Préparation pour l'analyse avec analyseur lxml
                        # On récupère ne liste les url des livres de cette catégorie
                        url_book_cat = f.list_book_cat(soup_cat, url_book_cat)
            else: # Si Nb_page n'est pas du type bs4.elemnt.Tag, c'est qu'il n'y a qu'une page
                # On récupère en liste les url des livres de cette catégorie
                url_book_cat = f.list_book_cat(soup_cat, url_book_cat)

        # Récupération des données de tous les livres d'une catégorie
        for url in url_book_cat:
            f.data_one_book(url, cat) # Ecriture des données pour ce livre dans le fichier scv de la catégorie
            time.sleep(0.5)
        print(len(url_book_cat))
time2 = time.process_time()
print(time2 - time1)

os.system("pause") # met en pause pour éviter la fermeture de la fenêtre d'excécution
# -*-coding:Utf-8 -*


import requests # module qui permet d'interagir avec une url

import bs4

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web

# Gestion des exceptions sur la requête
def validation_url(url):
    # Par défaut la requête est invalidée
    valide = False
    # Initialisation de la réponse de la requête. Reste vide si la requête est invalidée
    resp = requests.models.Response()
    try:
        resp = requests.get(url, timeout = 3) # timeout permet d'arréter la requête si le réponse tarde trop
        resp.raise_for_status()
    except requests.exceptions.InvalidSchema:
        print("L'adresse saisie est invalide")    
    except requests.exceptions.InvalidURL:
        print("L'adresse saisie est invalide")    
    except requests.exceptions.Timeout: # Exception levée si le timeout de réponse (réception des premières données) est dépassé
        print('La requête est trop longue. Le site ne répond pas.')
    except requests.exceptions.HTTPError as e: # Erreur de type 40X ou 50X
        print("La page n'existe pas ou bien le serveur ne répons pas. Erreur: ", e)
    except requests.exceptions.ConnectionError: # Exception levée si il y problème de connexion au réseau
        print("La connexion au réseau a échouée")
    else: # si le code de statut est 200
        if resp.ok: # le code de statut est 200
            # print("La requete s'est bien passée. Status-code: ", response.status_code )
            valide = True
    return(valide, resp)


# Ecriture de la ligne des entête dans fichier csv 
def Entete_csv_cat(fichier_csv_cat):
    # Initialisatin du fichier csv des livres d'une catégorie avec la ligne des entêtes
    with open(fichier_csv_cat, "w") as fichier_book:
        fichier_book.write("product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url\n")


# Récupère les données d'un livre
def data_one_book(url, categorie):
    valid_url, response = validation_url(url)
    if valid_url:
        soup_book = BeautifulSoup(response.text, 'lxml') # Préparation pour l'analyse avec analyseur lxml   
        title = soup_book.find("div", {"class" : "col-sm-6 product_main"}).find("h1") # On recherche le titre
        category = soup_book.find("ul", {"class" : "breadcrumb"}).findAll("a")[2] # On recherche la catégorie    
        product_description = soup_book.find("article", {"class" : "product_page"}).findAll("p")[3] # On recherche le résumé du livre    
        link_image = soup_book.find("div", {"class" : "item active"}).find("img") # On recherche l'url de l'image
        image_url = "http://books.toscrape.com/" + link_image['src'].replace("../", '') # On établit l'url complètle    
        Prod_Info = soup_book.find("table", {"class" : "table table-striped"}).findAll("tr") # Recherche des données Product Information
        # Pour chaque ligne de extract on crée une clé et une valeur dans Book_dico
        info_liste = []
        for tr in Prod_Info:
            info_liste.append(tr.find("td").text)
        # Ecriture dans le fichier csv des données demandées, dans l'ordre des entêtes
        with open(categorie + '.csv', "a") as fichier_book:
            fichier_book.write(
            url + ' , ' +                                        # url page livre
            info_liste[0] + ', ' +                               # Numéro UPC       
            title.text.replace(',', '-') + ', ' +                # Titre : supression d'éventuelles virgules du titre
            info_liste[3].replace('Â£', '') + ' £' + ', ' +      # Prix avec taxes - mise ne forme du prix
            info_liste[2].replace('Â£', '') + ' £' + ', ' +      # Prix sans taxes - mise ne forme du prix
            info_liste[5] + ', ' +                               # Quantité en stock
            product_description.text.replace(',', '-') + ', ' +  # Description - suppression virgules dans texte (remplacées par tirets)
            category.text + ', ' +                               # Catégorie
            info_liste[6] + ', ' +                               # review rating
            image_url + '\n')                                    # url image livre
    


def list_book_cat(soup, liste):
    # Recherche des url de chaque livre
    book_links = soup.findAll("div", {'class' : 'image_container'})
    # Pour chaque livre on rajoute l'url du livre à la liste des url de cette catégorie
    for div in book_links:
        a = div.find('a') 
        liste.append('http://books.toscrape.com/catalogue/' +  a['href'].replace("../", ''))
    return(liste)
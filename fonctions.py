# -*-coding:Utf-8 -*


import os
import requests # module qui permet d'interagir avec une url
import bs4 # import tout bs4 pour test type objet

import constantes as c

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web


def validation_url(url):
    """
    Cette fonction permet de vérifier la validité de l'url portée en paramètre.
    Elle essaye de lancer une requête avec le module requests.
    Un message est renvoyé si une exception est levée. 
    La fonction renvoie deux variables:

    Args:
        string : url de la page testée

    Return:
        bool : True si la raquête c'est bien passée, False dans le cas contraire
        response : résultat de la requête. Résultat vide si la requête s'est mal passée

    Raises:
        InvalidSchema:  si l'url saisie est invalide. Il manque http:// ou https:// au début
        InvalidURL:  l'url saisie n'est pas reconnue comme une url
        Timeout:  si il n'y a aucun début de réponse à la requête au bout de 3s 
        HTTPError: La page n'existe pas ou bien le serveur ne répond pas. Erreurs de type 40X ou 50X.
        ConnectionError: problème de connexion au réseau

    """
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


def navigation_dossier(type):
    """
    Cette fonction permet la navigation vers un dossier fichier_type.
    Le paramètre de la fonction est une chaine de caractère.
    Si le dossier n'existe pas encore il est créé.

    Args: 
        string: désigne le genre de fichiers rangés dans ce dossier. 'csv' ou bien 'img'

    Raises: 
        FileNotFoundError: dans le cas où le dossier n'existe pas encore. Il est alors créé.

    """
    # try navigation vers dossier de sauvegarde
    try:
        os.chdir("fichiers_" + type)
    # si échec créer dossier puis navigation
    except FileNotFoundError: 
        os.mkdir("fichiers_" + type)
        os.chdir("fichiers_" + type)


def entete_csv_cat(fichier_csv_cat):
    """
    Cette fonction permet l'écriture de l'entête du fichier csv pour une catégorie de livre.

    Args: 
        string: nom du fichier avec son extension

    """
    # Initialisatin du fichier csv des livres d'une catégorie avec la ligne des entêtes
    navigation_dossier('csv') # Navigation vers le dossier fichiers_csv
    with open(fichier_csv_cat, "w", encoding="utf-8") as fichier_book:
        fichier_book.write("product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url\n")
    os.chdir(os.pardir)


def data_one_book(url, categorie):
    """
    Cette fonction récupère les données d'un livre.
    Elle stocke les données dans un fichier csv correspondant à la catégorie du livre.
    Tous les fichiers csv sont rangés dans le dossier fichiers_csv.

    Args:
        string: url de la page des détails d'un livre
        string: catégorie du livre

    """
    valid_url, response = validation_url(url)
    response.encoding = response.apparent_encoding   # forçage de l'encodage vers utf-8 au lieu de ISO-8859-1
    if valid_url:
        soup_book = BeautifulSoup(response.text, 'lxml') # Préparation pour l'analyse avec analyseur lxml
        title = soup_book.find("div", {"class" : "col-sm-6 product_main"}).find("h1") # On recherche le titre
        category = soup_book.find("ul", {"class" : "breadcrumb"}).find_all("a")[2] # On recherche la catégorie    
        product_description = soup_book.find("article", {"class" : "product_page"}).find_all("p")[3] # On recherche le résumé du livre   
        link_image = soup_book.find("div", {"class" : "item active"}).find("img") # On recherche l'url de l'image
        image_url = c.URL_INDEX + link_image['src'].replace("../", '') # On établit l'url complète    
        prod_info = soup_book.find("table", {"class" : "table table-striped"}).find_all("tr") # Recherche des données Product Information
        # Pour chaque ligne de extract on crée une clé et une valeur dans Book_dico
        info_liste = []
        for tr in prod_info:
            info_liste.append(tr.find("td").get_text())
        # Ecriture dans le fichier csv des données demandées, dans l'ordre des entêtes
        navigation_dossier('csv')  # On se met dans le dossier fichiers_csv
        with open(categorie + '.csv', "a", encoding="utf-8") as fichier_book:
            fichier_book.write(
            url + ' , ' +                                                            # url page livre
            info_liste[0] + ', ' +                                                   # Numéro UPC       
            title.get_text().replace(',', '').replace(';', '') + ', ' +              # Titre : supression d'éventuelles virgules du titre
            info_liste[3] + ', ' +                                                   # Prix avec taxes - mise ne forme du prix
            info_liste[2] + ', ' +                                                   # Prix sans taxes - mise ne forme du prix
            info_liste[5] + ', ' +                                                   # Quantité en stock
            product_description.get_text().replace(',', '').replace(';', '') + ', ' +# Description - mise en forme par fonction encodage()
            category.get_text() + ', ' +                                             # Catégorie
            info_liste[6] + ', ' +                                                   # review rating
            image_url + '\n')                                                        # url image livre
        # navigation vers le dossier parent
        os.chdir(os.pardir)


def list_book_cat(soup, liste):
    """
    Cette fonction stocke dans une objet de type liste les url des livres d'une catégorie.
 
    Args: 
        soup: objet BeautifulSoup résultant de la requête sur une des page des livres d'une catégorie
        list: la liste des url déjà existantes.

    Return: 
        list: la liste des urlmise à jour.

    """
    # Recherche des url de chaque livre
    book_links = soup.find_all("div", {'class' : 'image_container'})
    # Pour chaque livre on rajoute l'url du livre à la liste des url de cette catégorie
    for div in book_links:
        a = div.find('a') 
        liste.append('http://books.toscrape.com/catalogue/' +  a['href'].replace("../", ''))
    return(liste)


def nombre_page_categorie(soup):
    """
    Cette fonction détermine le nombre de pages de livres pour une catégorie.

    Args: 
        soup: objet BeautifulSoup résultant de la requête sur la première page des livres d'un catégorie.

    Return:
        int:  nombre de pages.

    """
    # Recherche s'il y a plusieurs pages
    nb_page = soup.find("li", {"class" : "current"})
    # Si il y a plusieurs pages, un élément a été trouvé et alors nb_page est du type bs4.element.Tag
    if isinstance(nb_page, bs4.element.Tag):
        # On récupère le nombre de pages:
        nb_page = int(nb_page.get_text().strip()[-1])        
    else:
        nb_page = 1
    return(nb_page)


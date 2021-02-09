# -*-coding:Utf-8 -*


import os  # module système pour navigation dans arborescence dossiers
import requests  # module qui permet d'interagir avec une url
import bs4  # import tout bs4 pour test type objet
import time  # Permet ajout delai dans exécution code pour éviter de faire saturer le site en requêtes
import enlighten  # Pour la visualisation de la progression de l'extraction par bare de progression
import wget  # Pour le téléchargement des images des fichiers

from bs4 import BeautifulSoup  # bibliothèque qui permet de récupérer facilement des informations à partir de pages Web
from math import ceil  # Pour mettre ne forme le nom des fichiers image avec un nb limité de mots


# ************************************ #
# **********   CONSTANTES   ********** #
# ************************************ #


URL_INDEX = 'http://books.toscrape.com/'


# ************************************ #
# **********   FONCTIONS   *********** #
# ************************************ #


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
        resp = requests.get(url, timeout=3)  # timeout permet d'arréter la requête si le réponse tarde trop
        resp.raise_for_status()
    except requests.exceptions.InvalidSchema:
        print("L'adresse saisie est invalide")
    except requests.exceptions.InvalidURL:
        print("L'adresse saisie est invalide")
    except requests.exceptions.Timeout:  # Exception levée si le timeout de réponse (réception des premières données) est dépassé
        print('La requête est trop longue. Le site ne répond pas.')
    except requests.exceptions.HTTPError as e:  # Erreur de type 40X ou 50X
        print("La page n'existe pas ou bien le serveur ne répons pas. Erreur: ", e)
    except requests.exceptions.ConnectionError:  # Exception levée si il y problème de connexion au réseau
        print("La connexion au réseau a échouée")
    else:  # si le code de statut est 200
        if resp.ok:  # le code de statut est 200
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


def dossiers_images(cat):
    try:
        os.chdir(cat)
    # si échec créer dossier puis navigation
    except FileNotFoundError:
        os.mkdir(cat)
        os.chdir(cat)


def entete_csv_cat(fichier_csv_cat):
    """
    Cette fonction permet l'écriture de l'entête du fichier csv pour une catégorie de livre.

    Args:
        string: nom du fichier avec son extension

    """
    # Initialisatin du fichier csv des livres d'une catégorie avec la ligne des entêtes
    navigation_dossier('csv')  # Navigation vers le dossier fichiers_csv
    with open(fichier_csv_cat, "w", encoding="utf-8") as fichier_book:
        fichier_book.write("product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url\n")
    os.chdir(os.pardir)


def titre_fichier_image(titre):
    """
    Cette fonction met en forme le titre du livre résupérées parmis les données sur la page du livre
    Le résultat doit servir de nom de fichier au fichier image téléchargé

    Args:
        string : titre récupéré sur la page de description du livre

    Return:
        string: titre raccourci(maxi 5 mots), sans carcatères non autorisés

    """
    # Liste de caractères indésirables dans le nom de fichier de l'image
    filtre_carcateres = [',', ';', '’', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for caractere in filtre_carcateres:
        titre = titre.replace(caractere, '')  # Nettoie le titre
    title_liste = titre.split()
    # Détermine le nombre de mots du nom de l'image
    if len(title_liste) > 10:
        nb_mots_title_img = 5
    elif len(title_liste) > 6:
        nb_mots_title_img = ceil(len(title_liste)/2)
    else:
        nb_mots_title_img = len(title_liste)
    # Reconstruit un titre avec maximum les 5 premiers mots et des tirets entre
    title_img = "_".join(title_liste[:nb_mots_title_img])  
    return(title_img)


def data_one_book(url, categorie):
    """
    Cette fonction récupère les données d'un livre.
    Elle transforme les données brutes extraites.
    Elle stocke les données dans un fichier csv correspondant à la catégorie du livre.
    Tous les fichiers csv sont rangés dans le dossier fichiers_csv.
    Toutes les images des livres sont rangées dans le dossier fichiers_img

    Args:
        string: url de la page des détails d'un livre
        string: catégorie du livre

    """
    valid_url, response = validation_url(url)
    response.encoding = response.apparent_encoding   # forçage de l'encodage vers utf-8 au lieu de ISO-8859-1
    if valid_url:
        soup_book = bs4.BeautifulSoup(response.text, 'lxml')  # Préparation pour l'analyse avec analyseur lxml
        title = soup_book.find("div", {"class": "col-sm-6 product_main"}).find("h1")  # On recherche le titre
        review_rating = soup_book.find("div", {"class": "col-sm-6 product_main"}).find_all("p")[2]  # On cherche la notation
        category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2]  # On recherche la catégorie
        product_description = soup_book.find("div", {"id": "product_description"})  # On recherche le résumé du livre
        link_image = soup_book.find("div", {"class": "item active"}).find("img")  # On recherche l'url de l'image
        image_url = URL_INDEX + link_image['src'].replace("../", '')  # On établit l'url complète
        prod_info = soup_book.find("table", {"class": "table table-striped"}).find_all("tr")  # Recherche des données Product Information
        # On vérifie la présence d'une description.
        if isinstance(product_description, bs4.element.Tag):
            product_description = soup_book.find("div", {"id": "product_description"}).find_next("p").get_text()
        else:  # Si pas de description on met RAS dans la colonne correspodante du fichier csv
            product_description = "RAS"
        # Pour chaque ligne de extract on crée une clé et une valeur dans Book_dico
        info_liste = []
        for tr in prod_info:
            info_liste.append(tr.find("td").get_text())
        # Dictionnaire de correspondance notation / nombre d'étoiles
        notation = {'One': '*', 'Two': '**', 'Three': '***', 'Four': '****', 'Five': '*****'}
        # Ecriture dans le fichier csv des données demandées, dans l'ordre des entêtes
        navigation_dossier('csv')  # On se met dans le dossier fichiers_csv
        with open(categorie + '.csv', "a", encoding="utf-8") as fichier_book:
            fichier_book.write(
                url + ' , ' +  # url page livre
                info_liste[0] + ', ' +  # Numéro UPC
                title.get_text().replace(',', '').replace(';', '') + ', ' +  # Titre
                info_liste[3] + ', ' +  # Prix avec taxes
                info_liste[2] + ', ' +  # Prix sans taxes
                info_liste[5] + ', ' +  # Quantité en stock
                product_description.replace(',', ' ').replace(';', '-') + ', ' +  # Description
                category.get_text() + ', ' +  # Catégorie
                notation[review_rating['class'][1]] + ', ' +  # review rating
                image_url + ' \n')  # url image livre
        # navigation vers le dossier parent
        os.chdir(os.pardir)
        # Mise en forme du titre court pour nom du fichier image
        titre_image = titre_fichier_image(title.get_text()) + '.jpg'
        # navigation vers le dossier de stockage des images
        navigation_dossier('img')
        dossiers_images(categorie)
        # On télécharge l'image si elle n'existe pas encore. Sinon on passe
        try:
            with open(titre_image, "rb"):
                pass
        except FileNotFoundError:            
            # téléchargerment de l'image
            wget.download(image_url, out=titre_image)
        # navigation vers le dossier parent
        os.chdir(os.pardir)
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
    book_links = soup.find_all("div", {'class': 'image_container'})
    # Pour chaque livre on rajoute l'url du livre à la liste des url de cette catégorie
    for div in book_links:
        a = div.find('a')
        liste.append('http://books.toscrape.com/catalogue/' + a['href'].replace("../", ''))
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
    nb_page = soup.find("li", {"class": "current"})
    # Si il y a plusieurs pages, un élément a été trouvé et alors nb_page est du type bs4.element.Tag
    if isinstance(nb_page, bs4.element.Tag):
        # On récupère le nombre de pages:
        nb_page = int(nb_page.get_text().strip()[-1])
    else:
        nb_page = 1
    return(nb_page)


def cascade_extractions(url_site):
    """
    Fonction contenant l'extraction successive des catégories des livres,
    puis de tous livres de cette catégorie, répartis éventuellement surplusieurs page.
    La fonction lance ensuite l'extraction des données de chaque livre
    pour enregistrement dans des fichiers de stockage des données

    Args:
        string: url de la page d'acceuil du site

    """
    # Gestion des exceptions sur la requete
    valid_url, response = validation_url(url_site)
    # Construction de la liste des catégories à partir de la page accueuil du site
    if valid_url:
        # On prépare pour analyse
        soup_index = BeautifulSoup(response.text, "lxml")  # Préparation pour analyse avec analyseur lxml
        liste_li = soup_index.find('ul', {'class': "nav nav-list"}).find('ul').find_all('li')
        # On boucle sur toutes les catégories
        for li in liste_li:
            a = li.find('a')
            cat = a.get_text().strip()
            url_cat = URL_INDEX + a['href']
            # print(cat)
            # Création du fichier csv pour une catégorie
            entete_csv_cat(cat + '.csv')  # Ecriture entêtes dans fichier csv
            # Initialisation de la liste des url des livres pour cette catégorie
            url_book_cat = []
            valid_url, response = validation_url(url_cat)
            if valid_url:
                # On prépare pour analyse
                soup_cat = BeautifulSoup(response.text, "lxml")  # Préparation pour analyse
                # Recherche du nombre de pages:
                nombre_pages = nombre_page_categorie(soup_cat)

                if nombre_pages > 1:
                    # Pour chaque page on récupère les url des livres dans une liste
                    for i in range(1, nombre_pages + 1):
                        # On met en forme l'url de la page i:
                        url_cat_p = url_cat.replace("index.html", '') + "page-" + str(i) + ".html"
                        valid_url_p, response = validation_url(url_cat_p)
                        if valid_url_p:
                            # On prépare pour analyse
                            soup_cat = BeautifulSoup(response.text, "lxml")  # Préparation pour analyse
                            # On récupère en liste les url des livres de cette catégorie
                            url_book_cat = list_book_cat(soup_cat, url_book_cat)
                else:  # Si nb_page n'est pas du type bs4.elemnt.Tag, c'est qu'il n'y a qu'une page
                    # On récupère en liste les url des livres de cette catégorie
                    url_book_cat = list_book_cat(soup_cat, url_book_cat)

            # Récupération des données de tous les livres d'une catégorie
            for url in url_book_cat:
                # Ecriture des données pour ce livre dans le fichier scv de la catégorie
                data_one_book(url, cat)
                time.sleep(0.5)
                pbar.update()


# ************************************ #
# *************   MAIN   ************* #
# ************************************ #


if __name__ == "__main__":

    # Paramétrage bare de progression
    pbar = enlighten.Counter(total=1000, desc='Colorized', unit='ticks', color='seagreen1')

    # Excécution programme principal
    url_site = URL_INDEX + "index.html"
    cascade_extractions(url_site)

    os.system("pause")  # met en pause pour éviter fermeture fenêtre d'excécution

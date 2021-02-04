# -*-coding:Utf-8 -*


import requests # module qui permet d'interagir avec une url


def validation_url(url):
    # On gère les exceptions
    url_valide = False
    response = requests.models.Response()
    try:
        response = requests.get(url, timeout = 6) # timeout permet d'arréter la requête si le réponse tarde trop
        response.raise_for_status()
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
    else: # si le code de statut est 200 on annonce que tout s'est bien passé
        if response.ok: # le code de statut est 200
            # print("La requete s'est bien passée. Status-code: ", response.status_code )
            url_valide = True
    return(url_valide, response)


# Ecriture de la ligne des entête dans fichier csv 
def Entete_csv_cat(fichier_csv_cat):
    # Initialisatin du fichier csv des livres d'une catégorie avec la ligne des entêtes
    with open(fichier_csv_cat, "w") as fichier_book:
        fichier_book.write("product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url\n")


def data_one_book(url, catetogie):    
    validation_url, response_book = validation_url(url)    # Gestion des exception sur la requête sur l'url:
    soup_book = BeautifulSoup(response_book.text, 'lxml') # Préparation pour l'analyse avec analyseur lxml   
    title = soup_book.find("div", {"class" : "col-sm-6 product_main"}).find("h1") # On recherche le titre
    category = soup_book.find("ul", {"class" : "breadcrumb"}).findAll("a")[2] # On recherche la catégorie    
    product_description = soup_book.find("article", {"class" : "product_page"}).findAll("p")[3] # On recherche le résumé du livre

    # On recherche l'url de l'image
    link_image = soup_book.find("div", {"class" : "item active"}).find("img")
    image_url = "http://books.toscrape.com/" + link_image['src'].replace("../", '')

    # Recherche des données Product Information
    Prod_Info = soup_book.find("table", {"class" : "table table-striped"}).findAll("tr")

    # Pour chaque ligne de extract on crée une clé et une valeur dans Book_dico
    info_liste = []
    for tr in Prod_Info:
        info_liste.append(tr.find("td").text)

    # Ecriture dans le fichier csv des données demandées, dans l'ordre
    with open(cat + '.csv', "a") as fichier_book:
        fichier_book.write(url + ' , ' + 
        info_liste[0] + ', ' +
        title.text + ', ' +
        info_liste[3].replace('Â£', '') + ' £' + ', ' +
        info_liste[2].replace('Â£', '') + ' £' + ', ' +
        info_liste[5] + ', ' +
        product_description.text.replace(',', '-') + ', ' +
        category.text + ', ' +
        info_liste[6] + ', ' +
        image_url + '\n')



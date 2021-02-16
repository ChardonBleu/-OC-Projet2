# -*-coding:Utf-8 -*


import os  # module système pour navigation dans arborescence dossiers
import bs4  # import tout bs4 pour test type objet
import wget  # Pour le téléchargement des images des fichiers

from settings.constantes import URL_INDEX

from fonctions.requete import validation_url
from fonctions import navigation_stockage as nav


# ************************************************************************ #
# *********   Extraction et sauvegarde des données d'un livre   ********** #
# ************************************************************************ #


def data_one_book(url, categorie):
    """
    Cette fonction récupère les données d'un livre.
    Elle transforme les données brutes extraites.
    Elle stocke les données dans un fichier csv correspondant à la catégorie
    du livre.
    Tous les fichiers csv sont rangés dans le dossier fichiers_csv.
    Toutes les images des livres sont rangées dans le dossier fichiers_img

    Args:
        string: url de la page des détails d'un livre
        string: catégorie du livre

    """
    valid_url, response = validation_url(url)
    # forçage de l'encodage vers utf-8 au lieu de ISO-8859-1
    response.encoding = response.apparent_encoding
    if valid_url:
        # Préparation pour l'analyse avec analyseur lxml
        soup_book = bs4.BeautifulSoup(response.text, 'lxml')
        # On recherche le titre
        title = soup_book.find("div", {"class": "col-sm-6 product_main"}).find("h1")
        # On recherche la notation
        review_rating = soup_book.find("div", {"class": "col-sm-6 product_main"}).find_all("p")[2]
        # On recherche la catégorie
        category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
        # On recherche le résumé du livre
        product_description = soup_book.find("div", {"id": "product_description"})
        # On recherche l'url de l'image
        link_image = soup_book.find("div", {"class": "item active"}).find("img")
        # Recherche des données Product Information
        prod_info = soup_book.find("table", {"class": "table table-striped"}).find_all("tr")
        # Traitement des données extraites
        # On établit l'url complète
        image_url = URL_INDEX + link_image['src'].replace("../", '')
        # On vérifie la présence d'une description.
        if isinstance(product_description, bs4.element.Tag):
            product_description = soup_book.find("div", {"id": "product_description"}).find_next("p").get_text()
        else:
            product_description = "RAS"
        # Pour chaque ligne de prod_info on récupère texte entrebalises <td>.
        info_liste = []
        for tr in prod_info:
            info_liste.append(tr.find("td").get_text())
        # Dictionnaire de correspondance notation / nombre d'étoiles
        notation = {'One': '*', 'Two': '**', 'Three': '***',
                    'Four': '****', 'Five': '*****'}
        # Ecriture dans le fichier csv des données demandées
        nav.navigation_dossier('csv')
        with open(categorie + '.csv', "a", encoding="utf-8") as fichier_book:
            fichier_book.write(
                url + ' , ' +
                info_liste[0] + ', ' +  # Numéro UPC
                title.get_text().replace(',', '').replace(';', '') + ', ' +
                info_liste[3] + ', ' +  # Prix avec taxes
                info_liste[2] + ', ' +  # Prix sans taxes
                info_liste[5] + ', ' +  # Quantité en stock
                product_description.replace(',', ' ').replace(';', '-') + ', ' +
                category.get_text() + ', ' +
                notation[review_rating['class'][1]] + ', ' +
                image_url + ' \n')
        # navigation vers le dossier parent
        os.chdir(os.pardir)
        # Mise en forme du titre court pour nom du fichier image
        titre_image = nav.titre_fichier_image(title.get_text()) + '.jpg'
        # navigation vers le dossier de stockage des images
        nav.navigation_dossier('img')
        nav.dossiers_images(categorie)
        # On télécharge l'image si elle n'existe pas encore. Sinon on passe
        try:
            with open(titre_image, "rb"):
                pass
        except FileNotFoundError:
            nav.telecharge_image(image_url, titre_image)
        # navigation vers le dossier parent
        os.chdir(os.pardir)
        os.chdir(os.pardir)

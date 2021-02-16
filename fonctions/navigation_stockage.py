# -*-coding:Utf-8 -*


import os  # module système pour navigation dans arborescence dossiers
import wget  # Pour le téléchargement des images des fichiers
import urllib

# Pour mettre en forme le nom des fichiers image avec un nb limité de mots
from math import ceil


# ************************************************************************* #
# ******   Navigation vers les fichiers de sauvegarde des données   ******* #
# ************************************************************************* #


def navigation_dossier(type):
    """
    Cette fonction permet la navigation vers un dossier fichier_type.
    Le paramètre de la fonction est une chaine de caractère.
    Si le dossier n'existe pas encore il est créé.

    Args:
        string: désigne le genre de fichiers rangés dans ce dossier. 'csv'
        ou bien 'img'

    Raises:
        FileNotFoundError: dans le cas où le dossier n'existe pas encore.
        Il est alors créé.

    """
    # try navigation vers dossier de sauvegarde
    try:
        os.chdir("fichiers_" + type)
    # si échec créer dossier puis navigation
    except FileNotFoundError:
        os.mkdir("fichiers_" + type)
        os.chdir("fichiers_" + type)


def dossiers_images(cat):
    """
    Cette fonction permet la navigation vers un dossier image
    associé à la catégorie de livre.
    Le paramètre de la fonction indique la catégorie de livres.
    Si le dossier n'existe pas encore il est créé.

    Args:
        string: la catégorie de livre

    Raises:
        FileNotFoundError: dans le cas où le dossier n'existe pas encore.
        Il est alors créé.

    """
    try:
        os.chdir(cat)
    # si échec créer dossier puis navigation
    except FileNotFoundError:
        os.mkdir(cat)
        os.chdir(cat)


def titre_fichier_image(titre):
    """
    Cette fonction met en forme le titre du livre résupéré parmis les données
    sur la page du livre
    Le résultat doit servir de nom de fichier au fichier image téléchargé

    Args:
        string : titre récupéré sur la page de description du livre

    Return:
        string: titre raccourci(maxi 5 mots), sans carcatères non autorisés

    """
    # Liste de caractères indésirables dans le nom de fichier de l'image
    filtre_carcateres = [',', ';', '’', '/', '\\',
                         ':', '*', '?', '"', '<', '>', '|']
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
    # Reconstruit un titre avec maximum les 5 premiers mots et des underscore
    title_img = "_".join(title_liste[:nb_mots_title_img])
    return(title_img)


def telecharge_image(img_url, img_titre):
    try:
        wget.download(img_url, out=img_titre)
    except urllib.error.ContentTooShortError:
        print ('La connexion au réseau est instable. Reloading...')
        telecharge_image(img_url, img_titre)

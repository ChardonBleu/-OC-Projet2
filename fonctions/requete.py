# -*-coding:Utf-8 -*


import requests  # module qui permet d'interagir avec une url


# *********************************************************************************** #
# **********   Requête sur une url, avec gestion de quelques axceptions   *********** #
# *********************************************************************************** #


def validation_url(url):
    """
    Cette fonction permet de vérifier la validité de l'url portée en
    paramètre.
    Elle essaye de lancer une requête avec le module requests.
    Un message est renvoyé si une exception est levée.
    La fonction renvoie deux variables.

    Args:
        string : url de la page testée

    Return:
        bool : True si la raquête c'est bien passée, False dans le cas
        contraire
        response : résultat de la requête. Résultat vide si la requête
        s'est mal passée

    Raises:
        InvalidSchema:  si l'url saisie est invalide.
                        Il manque http:// ou https:// au début
        InvalidURL:  l'url saisie n'est pas reconnue comme une url
        Timeout:  si aucun début de réponse à la requête au bout de 3s
        HTTPError: La page n'existe pas ou bien le serveur ne répond pas.
                  Erreurs de type 40X ou 50X.
        ConnectionError: problème de connexion au réseau

    """
    # Par défaut la requête est invalidée
    valide = False
    # Initialisation de la réponse de la requête.
    resp = requests.models.Response()
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()  # Lève l'exception HTTPError
    except requests.exceptions.InvalidSchema:
        print("L'adresse saisie est invalide")
    except requests.exceptions.InvalidURL:
        print("L'adresse saisie est invalide")
    except requests.exceptions.Timeout:
        print('La requête est trop longue. Le site ne répond pas.')
    except requests.exceptions.HTTPError as e:
        print("La page n'existe pas ou le serveur ne réponds pas. Erreur:", e)
    except requests.exceptions.ConnectionError:
        print("La connexion au réseau a échouée")
    else:
        if resp.ok:  # le code de statut est 200
            valide = True
    return(valide, resp)

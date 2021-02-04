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


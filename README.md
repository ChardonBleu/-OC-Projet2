# Book_scraping
Le fichier extract_book.py est un programme de scraping du site exemple http://books.toscrape.com/index.html

Il extrait les données des 1000 livres du site et les enregistre dans des fichiers csv (un fichier par catégorie de livres).
Tous ces fichiers csv sont rangés dans un dossier fichiers_csv dans le même répertoire que le fichier extract_book.py.
Les images des livres sont également téléchargées et stockées dans un dossier fichiers_img dans ce même répertoire.

Enregistrer l'ensemble des fichiers dans un dossier local de votre choix.

Dans le terminal se mettre dans ce dossier local

Environnement virtuel
---
https://docs.python.org/fr/3/library/venv.html?highlight=venv

Créer un environnement virtuel: 

```bash
python -m venv env
```

Activer cet environnement virtuel:
sur windows dans Visual Studio Code: 
```bash 
. env/Scripts/activate 
```
sur mac ou linux: 
```bash 
source env/bin/activate 
```
Packages
---

Puis installer les modules necessaires:
```bash 
python -m pip -r requirements.txt
```

Exécution
---

Exécuter le fichier extract_book dans cet environnement virtuel.

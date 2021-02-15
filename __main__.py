# -*-coding:Utf-8 -*


import os  # module système pour navigation dans arborescence dossiers
import enlighten  # Pour visu progression extraction

from settings.constantes import URL_INDEX
from fonctions.categories import cascade_extractions


# ************************************ #
# *************   MAIN   ************* #
# ************************************ #


if __name__ == "__main__":

    # Paramétrage bare de progression
    pbar = enlighten.Counter(total=1000, desc='Colorized',
                             unit='ticks', color='seagreen1')

    # Excécution programme principal
    url_site = URL_INDEX + "index.html"
    cascade_extractions(url_site, pbar)

    os.system("pause")

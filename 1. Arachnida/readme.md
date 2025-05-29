# CyberPiscine #1: Arachnida


## Spider
> "The Spider program will allow you to extract all the images from a website, recursively, by providing a url as a parameter."

Spider scan le document html trouve via l'URL fournie, et recherche dans ce document toute mention d'image ou de lien menant vers une autre page.
Spider telecharge alors chaque image sur une page, puis va en visiter une autre, de facons recursive.

*(Creer un venv d'abord, voir section suivante)* <br>
Pour lancer Spider: `python3 spider.py (-r (-l [n])) (-p [path]) [URL]`<br>

`-r`: Telecharge recursivement.<br>
`-l [n]`: Details le niveau de la recursivite a la profondeur `n`. (default: 5)<br>
`-p [path]`: Fichier de sauvegarde les images. (./data/ par default)<br>
`[url]`: URL a fournir.

### Creation d'un Environement virtuel Python (Pour Spider)
Parce qu'on a besoin d'installer des dependances, on se creer un environnement virtuel par soucis de compatibilite.

Creation d'un virtual environement (venv): `python3 -m venv [nom]`<br>
Activer le venv:  `source [nom]/bin/activate`<br>
Desaciver le venv: `deactivate`<br>
Installation des requirements: `pip install requests beautifulsoup4 pillow piexif `

Une fois dans le venv, on peux lancer Spider.


## Scorpion
> The Scorpion program receives image files as parameters and must be able to parse them for EXIF and other metadatas, displaying them on the screen.

Scorpion analyse les images donnees, extirpe les metadonnees, et les affiche dans une interface graphique simpliste.

Pour lancer Scorpion: `python3 scorpion.py [file path] (+file path...)`
`[file path]`: Path vers l'image a analyser

Beaucoup des images d'internet sont nettoyer de leurs metadonnees.
Dans ce [repo](https://github.com/ianare/exif-samples/tree/master/jpg) se trouvent des images qui contiennent pour sur des metadonnees.

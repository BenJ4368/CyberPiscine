# CyberPiscine #1: Arachnida

En python, parce que c'est simple et que beaucoup de libraries utiles sont disponible.

(linux)<br>
Creation d'un virtual environement (venv): `python3 -m venv [nom]`<br>
Activer le venv:  `source [nom]/bin/activate`<br>
Desaciver le venv: `deactivate`
Installation des requirements: `pip install requests beautifulsoup4 pillow piexif `<br>

## Spider
> Extraire les images d'un site web recursivement

Spider.py: `python3 spider.py (-r (-l [n])) (-p [path]) [URL]`<br>
`-r`: Telecharge recursivement.<br>
`-l [n]`: Details le niveau de la recursivite a la profondeur `n`.<br>
`-p [path]`: Fichier de sauvegarde les images. (./data/ par default)<br>
`[url]`: j'ai besoin de l'expliquer?.


## Scorpion
> Extraire les metadata d'images.

Scorpion.py: `python3 scorpion.py [file path] (+file path...)`
`[file path]`: abuse, c'est dans le nom.

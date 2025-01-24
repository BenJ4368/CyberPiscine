# CyberPiscine #1: Arachnida

## Spider
>> Extraire les images d'un site web recursivement

En python, parce que c'est simple et que beaucoup de libraries utiles sont disponible.

(on linux)<br>
Creation d'un virtual environement (venv): `python3 -m venv [nom]`<br>
Activer le venv:  `source [nom]/bin/activate`<br>
Desaciver le venv: `deactivate`
Installation des requirements: `pip install requests beautifulsoup4`<br>
requirements.txt: `pip freeze > requirements.txt`, `pip install -r requirements.txt`, `pip list`

Spider.py : `python3 spider.py (-r (-l [n])) (-p [path]) [URL]`<br>
`-r`: Telecharge recursivement.<br>
`-l [n]`: Details le niveau de la recursivite a la profondeur `n`.<br>
`-p [path]`: Fichier de sauvegarde les images. (./data/ par default)<br>
`[ulr]`: URL cible.

## Scorpion
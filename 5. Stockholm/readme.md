# CyberPiscine #5: Stockholm

On fait les mechants maintenant?

## Stockholm
>> Creation d'un programme qui crypte des fichiers, facons malware.

### Le programme

On veux un programme qui crypte ou decrypte des fichiers en fonctions de leurs extensions, ou affiche des informations le concernant.<br><br>

On veux ces options:
- `-help, -h`: Affiche le descriptif.
- `-version, -v`: Affiche la version du programme.
- `-reverse, -r` decrypte les fichiers crypte precedement.
- `-silent, -s`: silence les output logs.

Pour `-help` et `-version`, on ne fait qu'ecrire en sortie.<br>
Pour crypter,  on selectionne les fichiers cibles (ceux localises dans `/home/infection/`, et dont les extensions correspondent aux cible de Wannacry, dont on parleras plus bas), on les copie en cryptant leurs contenu avec l'algorythme AES-128-CBC qui necessite une clef de 16 characters et en ajoutant l'extension `.ft`, puis on supprime les originaux. On se retrouve avec une floppee de fichier `.ft`, impossible a lire. On log chaque fichier crypter, sauf si `-silent` est applique.<br>
Pour decrypter, on utilise le meme algorythme avec la meme clef, on copie en decryptant et en supprimant l'exentions `.ft`, puis on supprime les fichiers cryptes. On log egalement les fichiers decrypter. Pas besoin de `-silent` ici, puisque c'est la fin de "l'attaque".


Les extensions qu'on doit cibler sont les memes qui ont ete cibles pendant l'attaque du ransomware `Wannacry` de Mai 2017; une cyberattaque d'envergure mondiale orchestree par la Core du Nord, qui utilisait une vulnerabilite des systeme windows non mis a jour ("EternalBlue") pour crypter des fichiers, et demandait une ransom pour le decryptage.
Une simple recherche google suffit pour trouver la liste des extensions qui ont ete cibles pendant Wannacry.

### Docker

`Make` suffit pour lancer l'environnement. Des fichiers (simplissime) sont deja present dans `/home/infection/`, dont certains ont et d'autres n'ont pas d'extensions cible. Il suffit alors de lancer le programme qui se trouve a la racine du container.



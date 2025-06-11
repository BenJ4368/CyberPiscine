# CyberPiscine #5 : 🕵️ Inquisitor

> Projet de Cybersécurité 42 : Création d'un programme qui usurpe l'identité d'une autre machine pour intercepter des paquets, "ARP poisoning".

## 🔧 Fonctionnalités

- Empoisonnement de la table ARP d'une victime.
- Restauration de la table ARP post-attaque.
- Interception et espionnage des paquets de fichiers transitoires.
- Bonus : Interception de tous les paquets transitoires.

### Mise en place

`Make` va lancer les 3 conteneurs qui vont simuler 3 machines différentes, dans un même réseau.

Ouvrons 3 terminaux supplémentaires :

- `make info` : Nous donne toutes les adresses dont nous allons avoir besoin.
- `make attacker` : Nous ouvre le conteneur `attacker`, d'où nous allons ensuite lancer l'attaque<br>
avec `python3 inquisitor.py [serverIP attackerMAC clientIP clientMAC]`.
- `make client` : Nous ouvre le conteneur `client`, avec lequel nous allons créer puis envoyer des fichiers via FTP au serveur.<br>
Ses fichiers vont en fait être redirigés vers Attacker.

Dans le conteneur `client` :<br>
Se connecter au serveur FTP : `ftp [serverIP] 21`<br>
Authentification : `serv_user`<br>
Mot de passe : `serv_pass`<br>
Pour créer des fichiers, nous allons repasser sur bash avec : `!`<br>
On crée quelques fichiers simples : `touch [filename]`<br>
On revient sur FTP : `exit`<br>
On envoie ses fichiers au serveur : `put [filename]`<br>
Pour voir les fichiers disponibles : `ls`<br>
Pour demander des fichiers depuis le serveur : `get [filename]`<br>
Besoin d'aide ? : `?`<br>

### 🧪 Testons

En envoyant nos fichiers vers le serveur FTP "directement" (nous avons bien spécifié l'adresse IP du serveur),<br> nous nous apercevons que notre `inquisitor` a reçu nos paquets, dont les noms des fichiers passés.<br>
`Inquisitor` s'est donc bien interposé entre le client et le serveur.

### Bonus

Le bonus ajoute simplement une option verbose à `inquisitor`, avec l'option `-v`.<br>
Le mode verbose fait qu'`inquisitor` affiche désormais tous les paquets qu'il intercepte, <br>et non uniquement les noms de fichiers.

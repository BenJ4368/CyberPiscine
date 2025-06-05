# CyberPiscine #3: 🧅 Onion

> Projet de cybersécurité 42 : Hébergement d'un site web statique (service caché) sur le réseau Tor, permettant un accès anonyme et sécurisé via une adresse en `.onion`.

---

## 🛠️ Details de configuration

On se sert d'un 🐳 Docker container pour ne pas etre limiter en  droit.
On y install Nginx, Tor et on y configure un acces ssh comme demande par le sujet (port 4242).
On configure Nginx pour desservir un Hidden Service de Tor en HTTP(80).


Demarrer le projet: `make`<br>
Ouvrir Tor: `cd Desktop/tor-browser && ./start-tor-browser.desktop`<br>
Recuperer l'adresse .onion: `make onionaddr`<br>
Copier cette addresse dans Tor pour se connecter au serveur. <br>

Pour se connecter en ssh:
Recuperer l'adresse IP: `make ipaddr`<br>
Etablir la Connexion SSH: `ssh root@<ip> -p 4242`<br>

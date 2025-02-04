# CyberPiscine #3: Onion

Docker !

## ft_onion
>> Heberger une simple page html, accessible sur Tor. Et connexion au serveur en ssh.

Lancer le serveur: `make`<br>
Ouvrir Tor: `cd Desktop/tor-browser && ./start-tor-browser.desktop`<br>
Onion Address: `make onionaddr`<br>
Copier cette addresse dans Tor pour se connecter au serveur.
IP Address: `make ipaddr`<br>
Connexion SSH: `ssh root@<ip> -p 4242`<br>
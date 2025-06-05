# CyberPiscine #2: 🔐 OTP

> Projet de cybersécurité 42 : chiffrement de clé et génération d'OTP

Ce projet implémente un système simple de génération de mots de passe à usage unique (OTP) basé sur une clé secrète chiffrée. Il permet de renforcer l'authentification en évitant l'utilisation de mots de passe statiques.

---

## 🛠️ Compilation
`g++ -std=c++17 -o ft_otp ft_otp.cpp -lssl -lcrypto`

## ⚙️ Fonctionnement

1. **Enregistrement de la clé** : L'utilisateur enregistre une clé secrète qui est chiffrée et stockée.
2. **Génération d'OTP** : À chaque demande, un mot de passe unique est généré à partir de la clé chiffrée.


Utilisation: `./ft_otp [-g <key> | -k]`<br>
`-g <key>`: Enregister et crypte `key`, qui doit etre au format hexadecimal et d'une longueur >=64.<br>
`-k`: Genere un OTP a partir de `key`.<br>

---

Verification avec aothtool (demande par le sujet): oathtool --totp `key`.
> Attention: pour oathtool, `key` ne doit pas etre cryptee

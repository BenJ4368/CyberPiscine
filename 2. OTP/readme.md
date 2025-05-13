# CyberPiscine #2: OTP

En cpp, parce que je connais mieu que le python.

## ft_otp
>> Enregister et crypter une clef, et s'en servir pour generer des mots de passe a usage unique.

Compilation: `g++ -std=c++17 -o ft_otp ft_otp.cpp -lssl -lcrypto`<br>
Utilisation: `./ft_otp [-g <key> | -k]`<br>
`-g <key>`: Enregister et crypte `key`, qui doit etre au format hexadecimal et d'une longueur >=64.<br>
`-k`: Genere un OTP a partir de `key`.<br>

Verification avec aothtool: oathtool --totp `key`.
> Attention: pour oathtool, `key` ne doit pas etre cryptee
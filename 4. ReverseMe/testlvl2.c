#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void no(void) {
    puts("Nope.");
    exit(1);
}

void ok(void) {
    puts("Good job.");
}

int main(void)
{
    char password[24];
    char key[9] = "d";  // Initialisation de key[0] à 'd' directement.
    int passwordOffset = 2;  // On commence à l'index 2 après "00"
    int i = 1;

    printf("Please enter key: ");
    if (scanf("%s", password) != 1 || password[0] != '0' || password[1] != '0') {
        no();
    }

    // Vérification que le mot de passe est suffisamment long pour permettre l'extraction des triplets
    int passwordLength = strlen(password);
    if (passwordLength < 9) {
        no();
    }

    while (i < 8 && passwordOffset + 2 < passwordLength) {
        // Copie des 3 caractères du mot de passe dans le buffer
        char buffer[4] = {password[passwordOffset], password[passwordOffset + 1], password[passwordOffset + 2], '\0'};
        key[i] = (char)atoi(buffer);  // Convertir le triplet de caractères en entier

        passwordOffset += 3;
        i++;
    }

    // S'assurer que le mot de passe correspond à "delabere"
    if (strcmp(key, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
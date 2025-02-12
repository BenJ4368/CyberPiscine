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
    printf("Please enter key: ");
    
    char password[24]; // 2 + 7*3 + 1
    if (scanf("%s", password) != 1 || password[0] != '0' || password[1] != '0') // 
        no();

    if (strlen(password) != 23) // Si c'est plus petit, on sait que ca marcheras pas, si c'est plus grand, ca peux segfault.
        no();

    char key[9] = "d"; // On declare un tableau de 9, puis on assigne 'd' sur key[0]. declaration != assignation
    int passwordOffset = 2;  // On commence à l'index 2 après "00"

    int i = 1;
    while (i < 8 && passwordOffset + 2 < (int)strlen(password)) {
        // Copie des 3 caractères de password dans un buffer
        char buffer[4] = {password[passwordOffset], password[passwordOffset + 1], password[passwordOffset + 2], '\0'};
        key[i] = (char)atoi(buffer);  // Convertir le triplet de caractères en entier, et le place dans key

        passwordOffset += 3;
        i++;
    }

    if (strcmp(key, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
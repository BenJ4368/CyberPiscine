#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void ok(void)
{
    puts("Good Job.\n");
}
void no(void)
{
    puts("Nope.\n");
    exit(1);
}

int main(void)
{
    printf("Please enter key: ");
    
    char password[100];
    if (scanf("%s", password) != 1 || password[0] != '4' || password[1] != '2')
        no();

    char key[8];
    key[0] = '*';
    int passwordOffset = 2;  // On commence à l'index 2 après "00"

    int i = 1;
    while (i < 7 && passwordOffset + 2 < (int)strlen(password)) {
        // Copie des 3 caractères de password dans un buffer
        char buffer[4] = {password[passwordOffset], password[passwordOffset + 1], password[passwordOffset + 2], '\0'};
        key[i] = (char)atoi(buffer);  // Convertir le triplet de caractères en entier, et le place dans key

        passwordOffset += 3;
        i++;
    }
    key[7] = '\0';

    if (strcmp(key, "*******") == 0)
        ok();
    else
        no();

    return 0;
}
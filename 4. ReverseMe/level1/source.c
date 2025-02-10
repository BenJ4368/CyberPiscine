#include <stdio.h>
#include <string.h>

int main() {
    char input[50];

    printf("Please enter key: ");
    
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    if (strcmp(input, "__stack_check") == 0) {
        printf("Good job.\n");
    } else {
        printf("Nope.\n");
    }
    return 0;
}

#include "stdio.h"

int main() {
    char bitstring[128 + 1];
    bitstring[128] = '\0';

    char byte = 0;
    for (int i = 0; i < 16; i++) {
        byte = (rand() % 256);
        for (int j = 7; j >= 0; j--) { // Побитовая запись байта в бит-строку
            if ((byte >> j) & 1) 
                bitstring[(7 - j) + i * 8] = '1';
            else
                bitstring[(7 - j) + i * 8] = '0';
        }
    }

    printf("%s", bitstring);

    FILE* output = fopen("output_c.txt", "w");
    if (output == NULL) {
        return 1;
    }
    fputs(bitstring, output);
    fclose(output);
    return 0;
}
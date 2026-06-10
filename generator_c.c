#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define BIT_COUNT 128

int main() {
    srand(time(NULL));
    FILE* f = fopen("sequences/sequence_c.txt", "w");
    if (f == NULL) {
        printf("Ошибка создания файла!\n");
        return 1;
    }
    for (long i = 0; i < BIT_COUNT; i++) {
        int bit = rand() % 2;
        fputc(bit == 1 ? '1' : '0', f);
    }
    fclose(f);
    printf("Готово! %d бит сохранено в sequences/sequence_c.txt\n", BIT_COUNT);
    return 0;
}

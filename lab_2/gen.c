#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(0));  // Инициализация генератора
    
    for (int i = 0; i < 128; i++) {
        printf("%d", rand() % 2);
    }
    printf("\n");
    
    return 0;
}

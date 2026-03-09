#include <stdio.h>
#include <stdint.h>
#include <time.h>

/**
 * Генератор Xorshift (алгоритм Джорджа Марсальи)
 * Очень быстрый и качественный ГПСЧ
 */
uint32_t xorshift32(uint32_t *state) {
    uint32_t x = *state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *state = x;
    return x;
}

int main() {
    FILE *file = fopen("sequence_c.txt", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Инициализация начальным значением (не нулём!)
    uint32_t state = time(NULL);
    if (state == 0) state = 123456789; // на всякий случай
    
    int N = 128; // длина последовательности
    
    printf("Sequence generation\n");
    
    for (int i = 0; i < N; i++) {
        uint32_t rand_num = xorshift32(&state);
        int bit = rand_num & 1; // берём младший бит
        fprintf(file, "%d", bit);
        
        // Для отладки (выводим каждые 32 бита)
        if ((i + 1) % 32 == 0) {
            printf("Generated %d bit\n", i + 1);
        }
    }
    
    fclose(file);
    printf("\nThe sequence is saved in sequence_c.txt\n");
    return 0;
}
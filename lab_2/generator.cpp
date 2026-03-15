#include <iostream>
#include <cstdlib>
#include <ctime>
#include <bitset>
#include <string>

int main() {
    // Инициализация генератора текущим временем
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    const int num_bits = 128;
    std::string binary_sequence = "";

    std::cout << "Сгенерированная последовательность (C++):" << std::endl;
    for (int i = 0; i < num_bits; ++i) {
        // Генерируем случайное число 0 или 1
        char bit = (std::rand() % 2) ? '1' : '0';
        binary_sequence += bit;
        std::cout << bit;
        // Для удобства чтения добавляем пробел между байтами
        if ((i + 1) % 8 == 0) std::cout << ' ';
    }
    std::cout << std::endl;
    return 0;
}
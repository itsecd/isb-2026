#include <iostream>
#include <random>
#include <bitset>

int main() {
    // Инициализация генератора с случайным стартовым числом
    std::random_device rd;
    std::mt19937_64 gen(rd());

    // Генерация 128-битной последовательности
    uint64_t part1 = gen();
    uint64_t part2 = gen();

    // Объединение в 128-битную последовательность
    std::bitset<128> sequence;
    for (int i = 0; i < 64; ++i) {
        sequence[i] = (part1 >> i) & 1ULL;
        sequence[i + 64] = (part2 >> i) & 1ULL;
    }

    std::cout << "128-битная последовательность: " << sequence << std::endl;

    return 0;
}
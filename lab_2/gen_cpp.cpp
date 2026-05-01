// gen_cpp.cpp
#include <iostream>
#include <fstream>
#include <random>
#include <cstdint>

int main() {
    const std::uint32_t seed = 12345u; // можно менять
    const int N = 128;

    std::mt19937 rng(seed);
    std::uniform_int_distribution<int> bit(0, 1);

    std::ofstream out("seq_cpp.txt");
    if (!out) {
        std::cerr << "Не удалось открыть файл seq_cpp.txt для записи\n";
        return 1;
    }

    for (int i = 0; i < N; ++i) {
        out << bit(rng);
    }
    out << "\n";

    std::cout << "Последовательность сохранена в seq_cpp.txt\n";
    return 0;
}
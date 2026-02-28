#include <iostream>
#include <fstream>
#include <random>
#include <cstdint>

int main() {
    const std::uint32_t seed = 12345u;
    const int N = 128;

    std::mt19937 rng(seed);
    std::uniform_int_distribution<int> bit(0, 1);

    std::ofstream out("seq_cpp.txt");
    if (!out) {
        std::cerr << "Failed to open file <seq_cpp.txt> for writing\n";
        return 1;
    }

    for (int i = 0; i < N; ++i) {
        out << bit(rng);
    }
    out << "\n";

    std::cout << "The sequence is saved in <seq_cpp.txt>\n";
    return 0;
}
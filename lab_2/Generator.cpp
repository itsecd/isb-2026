#include <iostream>
#include <random>
#include <string>

int main() {
    std::mt19937 rng(12345);
    std::uniform_int_distribution<int> dist(0, 1);
    std::string bits;
    bits.reserve(128);
    for (int i = 0; i < 128; ++i) {
        bits += std::to_string(dist(rng));
    }
    std::cout << bits << "\n";
    return 0;
}
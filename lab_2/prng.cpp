#include <iostream>
#include <random>
#include <fstream>

int main() {
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<int> dist(0, 1);

    std::ofstream file("bits_cpp.txt");

    for (int i = 0; i < 128; i++) {
        file << dist(gen);
    }

    file.close();
}
#include <iostream>
#include <fstream>
#include <random>

int main() {

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);

    std::ofstream file("../sequences/seq_cpp.txt");

    for (int i = 0; i < 128; i++) {
        int bit = dist(gen);

        std::cout << bit;
        file << bit;
    }

    file.close();
}
#include <iostream>
#include <fstream>
#include <random>

int main() {
    std::ofstream file("C++.txt");
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(0, 1);

    for (int i = 0; i < 128; i++) {
        file << dist(gen);
    }

    file.close();
    std::cout << "C++: C++.txt" << std::endl;
    return 0;
}
#include <iostream>
#include <vector>
#include <random>
#include <fstream>

int main() {
    const int N = 128;
    std::random_device rd; 
    std::mt19937 gen(rd()); 

    std::uniform_int_distribution<> dis(0, 1);

    std::ofstream file("seq_cpp.txt");
    if (!file.is_open()) {
        std::cerr << "Ошибка при открытии файла." << std::endl;
        return 1;
    }

    for (int i = 0; i < N; ++i) {
        file << dis(gen);
    }

    file.close();
    return 0;
}
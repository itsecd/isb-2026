#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>

int main() {
    std::ofstream file("sequence_cpp.txt");
    srand(time(0));
    int N = 128; // Длина последовательности для тестов

    for (int i = 0; i < N; i++) {
        file << rand() % 2;
    }
    file.close();
    std::cout << "The C++ sequence is stored in sequence_cpp.txt" << std::endl;
    return 0;
}
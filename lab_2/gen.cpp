#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    std::srand(std::time(0)); // Инициализация генератора
    std::string sequence = "";
    for (int i = 0; i < 128; ++i) {
        sequence += (std::rand() % 2) ? '1' : '0';
    }
    std::cout << sequence << std::endl;
    return 0;
}
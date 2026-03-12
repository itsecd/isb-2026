#include <iostream>
#include <bitset>
#include <random>
#include <fstream>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    
    std::bitset<128> sequence;
    
    std::cout << "Сгенерированная последовательность (C++):" << std::endl;
    for (int i = 0; i < 128; i++) {
        sequence[i] = dis(gen);
        std::cout << sequence[i];
    }
    std::cout << std::endl;
    

    std::ofstream outFile("sequence_cpp.txt");
    if (outFile.is_open()) {
        for (int i = 0; i < 128; i++) {
            outFile << sequence[i];
        }
        outFile.close();
        std::cout << "\nПоследовательность сохранена в файл: sequence_cpp.txt" << std::endl;
    } else {
        std::cout << "Ошибка при создании файла!" << std::endl;
    }
    
    return 0;
}
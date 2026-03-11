#include <iostream>
#include <fstream>
#include <random>
#include <string>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    
    std::string sequence = "";
    for (int i = 0; i < 128; ++i) {
        sequence += std::to_string(dis(gen));
    }
    
    std::cout << "C++ последовательность (128 бит):" << std::endl;
    std::cout << sequence << std::endl;
    
    std::ofstream outFile("sequence_cpp.txt");
    if (outFile.is_open()) {
        outFile << sequence;
        outFile.close();
        std::cout << "Сохранено в sequence_cpp.txt" << std::endl;
    }
    
    return 0;
}
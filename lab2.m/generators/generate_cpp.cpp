#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));
   
    std::ofstream file("../sequences/sequence_cpp.txt");
    if (file.is_open()) {
        for (int i = 0; i < 128; i++) {
            file << (rand() % 2);
        }
        file.close();
        std::cout << "Сохранено в ../sequences/sequence_cpp.txt" << std::endl;
    } else {
        std::cout << "Не удалось создать файл" << std::endl;
    }
    
    return 0;
}
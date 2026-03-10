#include <iostream>
#include <fstream>
#include <random>
#include <bitset>
#include <string>

int main() {
    // Инициализация генератора Mersenne Twister
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<uint32_t> dist(0, UINT32_MAX);

    std::ofstream write_file("sequence_cpp.txt");
    if (!write_file.is_open()) {
        std::cerr << "Ошибка открытия файла для записи!" << std::endl;
        return 1;
    }

    std::string binarySequence = "";
    int bitsNeeded = 128;
    int bitsPerInt = 32; // uint32_t дает 32 бита
    int iterations = bitsNeeded / bitsPerInt;

    for (int i = 0; i < iterations; ++i) {
        uint32_t number = dist(gen);
        // Преобразуем число в бинарную строку (32 бита)
        std::bitset<32> bits(number);
        binarySequence += bits.to_string();
    }

    // Запись в файл
    write_file << binarySequence;
    write_file.close();

    std::cout << "Generated Comlite. Write in sequence_cpp.txt" << std::endl;
    std::cout << "Result: " << binarySequence << std::endl;

    return 0;
}
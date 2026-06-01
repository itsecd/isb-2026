// lab_2/src/generators/generator.cpp
// Генератор псевдослучайной последовательности на C++
// Использует std::mt19937 (Mersenne Twister) — стандарт C++11

#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;

/**
 * Генерирует 128-битную бинарную последовательность
 * и сохраняет в файл с ОТНОСИТЕЛЬНЫМ путём
 */
int main() {
    // Инициализация генератора
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, 1);
    
    // Генерация 128 бит
    std::string sequence;
    sequence.reserve(128);
    
    for (int i = 0; i < 128; ++i) {
        sequence += std::to_string(distrib(gen));
    }
    
    // ✅ ОТНОСИТЕЛЬНЫЙ ПУТЬ: работает из любой директории
    fs::path output_path = fs::path("../../data/sequences/cpp_sequence.txt");
    fs::create_directories(output_path.parent_path());
    
    std::ofstream file(output_path);
    if (file.is_open()) {
        file << sequence;
        file.close();
        std::cout << "[C++] Generated: " << sequence << "\n";
        std::cout << "[C++] Saved: " << output_path << "\n";
    } else {
        std::cerr << "[C++] Error: Cannot open " << output_path << "\n";
        return 1;
    }
    
    return 0;
}
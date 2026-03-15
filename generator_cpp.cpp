#include <fstream>
#include <random>
#include "constants.hpp"

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    
    std::ofstream file(OUTPUT_FILENAME);
    
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        file << dis(gen);
    }
    
    file.close();
    return 0;
}
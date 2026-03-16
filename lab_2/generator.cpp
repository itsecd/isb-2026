#include <iostream>
#include <fstream>
#include <random>

void generate_sequence(const std::string& filename, int length) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);
    
    std::ofstream file(filename);
    
    for(int i = 0; i < length; i++) {
        file << dist(gen);
    }
    
    file.close();
}

int main() {
    generate_sequence("sequence_cpp.txt", 128);
    return 0;
}
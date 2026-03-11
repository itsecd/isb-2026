#include <iostream>
#include <random>
#include <fstream>


void createRandomSequence(int* sequence, size_t size) {
    std::random_device rd; 
    std::mt19937 gen(rd()); 
    std::uniform_int_distribution<> dis(0, 1); 

    for (size_t i = 0; i < size; i++) {
        sequence[i] = dis(gen);
    }
}


void writeFile(int* const sequence, size_t size) {
    std::ofstream file("../../lab_2/c++_sequence.txt");
    if (file.is_open()) {
        for (size_t i = 0; i < size; i++) {
            file << sequence[i];
        }
        file.close();
    }
    else {
        throw std::exception("File is not found");
    }
}


int main() {
    size_t size = 128;
    int* sequence = new int[size];

    createRandomSequence(sequence, size);
    try {
        writeFile(sequence, size);
    } catch (const std::exception& e) {
        std::cerr << e.what();
    }

    delete[] sequence;
}
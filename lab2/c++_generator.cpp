#include <iostream>
#include <fstream>
#include <random>
#include <string>


//генерирует псевдослучайную последовательность из 128 бит
std::string generate_random_sequence() {
    std::string sequence = "";

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0,1);

    for (int i = 0; i < 128; i++) {
        int sequence_element = dis(gen);
        sequence += std::to_string(sequence_element);
    }

    return sequence;
}


//записывает последовательность в файл
void write_file(std::string file_name, std::string sequence) {
    std::ofstream file(file_name);
    
    if (!file.is_open()) {
        throw std::runtime_error("Couldn't open the file");
    }
    else {
        file << sequence;
    }

    file.close();
}


int main() {
    std::string sequence = generate_random_sequence();
    write_file("c++_sequence.txt", sequence);
}
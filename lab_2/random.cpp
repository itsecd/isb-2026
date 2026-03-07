#include <fstream>
#include <iostream>
#include <random>
#include <string>


std::string generate_128() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<size_t> number(0, 1);

    std::string seq;
    for (size_t i = 0; i < 128; ++i) {
        seq += std::to_string(number(gen));
    }
    return seq;
}

void save_string(std::string dir, std::string seq) {
    try {
        std::ofstream out;
        out.open(dir);
        if (!out.is_open()) {
            throw std::runtime_error("failed to open file " + dir);
        }
        out << seq << std::endl;
        out.close();
    }
    catch (const std::exception& e) {
        std::cerr << "unknown error " << e.what() << std::endl;
        throw;
    }
}

int main() {
    std::string seq = generate_128();
    save_string("sequence_cpp.txt", seq);
    std::cout << seq;
}
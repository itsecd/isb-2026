#include <iostream>
#include <fstream>
#include <random>
#include <bitset>

int main() {
    std::mt19937 rand(42);

    std::string binary_string = "";
    uint8_t byte = 0;
    for (size_t i = 0; i < 16; i++) {
        byte = rand() % 256;
        binary_string += std::bitset<8>(byte).to_string();
    }
    std::cout << binary_string << "\n";

    std::ofstream output("output_cpp.txt");
    if(!output.is_open()) return -1;
    output << binary_string;
    output.close();
    return 0;
}
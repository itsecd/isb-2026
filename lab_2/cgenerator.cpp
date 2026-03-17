#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));
    
    std::ofstream file("sequence_cpp.txt");
    std::string seq;
    
    for(int i = 0; i < 128; i++) {
        char bit = rand() % 2 + '0';
        seq += bit;
        std::cout << bit;
    }
    
    file << seq;
    file.close();
    std::cout << "\n";
    
    return 0;
}
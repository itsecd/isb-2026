#include <iostream>
#include <fstream>
#include <random>

int main() {
    std::ofstream outFile("sequence.txt");
    std::random_device rd; 
    std::mt19937 gen(rd()); 
    std::uniform_int_distribution<> distrib(0, 1);

    for (int i = 0; i < 128; ++i) {
        outFile << distrib(gen);
    }
    
    outFile.close();
    return 0;
}
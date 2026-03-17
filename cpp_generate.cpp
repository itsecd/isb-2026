#include <iostream>
#include <fstream>
#include <bitset>
#include <random>
#include <vector>

using namespace std;

vector<bool> generateRandomBits() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);
    
    vector<bool> bits;
    bits.reserve(128);
    
    for (int i = 0; i < 128; i++) {
        bits.push_back(dis(gen) == 1);
    }
    
    return bits;
}

void saveToFile(const vector<bool>& bits, const string& filename) {
    ofstream file(filename);
    for (bool bit : bits) {
        file << (bit ? '1' : '0');
    }
    file.close();
}


int main() {

    vector<bool> bits1 = generateRandomBits();
    saveToFile(bits1, "sequence_mt19937.txt");
   
    return 0;
}
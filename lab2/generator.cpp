#include <iostream>
#include <fstream>
#include <random>
#include <chrono>
#include <string>
#include <direct.h>

using namespace std;

void createDirectory(const string& path) {
    _mkdir(path.c_str());
}

string generateBits(int length) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dist(0, 1);
    
    string bits = "";
    for (int i = 0; i < length; i++) {
        bits += (dist(gen) == 1 ? '1' : '0');
    }
    return bits;
}

int main() {
    createDirectory("sequences");
    
    string bits = generateBits(128);
    
    ofstream file("sequences/cpp_sequence.txt");
    file << bits;
    file.close();
    
    cout << "C++: sequence/cpp_sequence.txt (128 бит)" << endl;
    return 0;
}
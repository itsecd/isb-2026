#include <iostream>
#include <fstream>
#include <random>
#include <chrono>
#include <bitset>
#include <string>

using namespace std;

string generateSequenceLCG(int length) {
    unsigned int seed = chrono::system_clock::now().time_since_epoch().count();
    string sequence;
    
    for (int i = 0; i < length; i++) {
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        sequence += (seed % 2) ? '1' : '0';
    }
    return sequence;
}

string generateSequenceMT(int length) {
    unsigned int seed = chrono::system_clock::now().time_since_epoch().count();
    mt19937 gen(seed);
    uniform_int_distribution<> dis(0, 1);
    
    string sequence;
    for (int i = 0; i < length; i++) {
        sequence += to_string(dis(gen));
    }
    return sequence;
}

string generateSequenceRD(int length) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);
    
    string sequence;
    for (int i = 0; i < length; i++) {
        sequence += to_string(dis(gen));
    }
    return sequence;
}

int main() {
    const int LENGTH = 128;
    string seq1 = generateSequenceLCG(LENGTH);
    string seq2 = generateSequenceMT(LENGTH);
    string seq3 = generateSequenceRD(LENGTH);
    
    ofstream file("sequences_cpp.txt");
    file << "Sequence 1 (LCG): " << seq1 << endl;
    file << "Sequence 2 (MT): " << seq2 << endl;
    file << "Sequence 3 (RD): " << seq3 << endl;
    file.close();
    
    cout << "Generated sequences saved to sequences_cpp.txt" << endl;
    cout << "Sequence 1: " << seq1 << endl;
    cout << "Sequence 2: " << seq2 << endl;
    cout << "Sequence 3: " << seq3 << endl;
    
    return 0;
}
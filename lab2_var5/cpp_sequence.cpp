#include <fstream>
#include <random>
#include <iostream>

using namespace std;

int main() {
    random_device rd;
    mt19937_64 gen(rd());  
    uniform_int_distribution<int> dist(0, 1);

    ofstream fout("cpp_sequence.txt");
    if (!fout) {
        cerr << "Error: cannot create file\n";
        return 1;
    }
    
    constexpr int BITS = 128;
    for (int i = 0; i < BITS; ++i) {
        fout << dist(gen);
    }
    
    fout.close();
    
    return 0;
}
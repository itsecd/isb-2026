#include <iostream>
#include <fstream>
#include <string>
#include <random>

using namespace std;

int main() {
    try {
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<int> dist(0, 1);
        
        string bits = "";
        for (int i = 0; i < 128; i++) {
            bits += (dist(gen) == 0) ? '0' : '1';
        }
        
        ofstream file("cpp_posled.txt");
        if (!file.is_open()) {
            throw runtime_error("Failed to create a file cpp_posled.txt");
        }
        file << bits << endl;
        file.close();
        
        cout << "C++ sequence (128 bit):" << endl;
        for (size_t i = 0; i < bits.length(); i++) {
            cout << bits[i];
            if ((i + 1) % 8 == 0 && i != bits.length() - 1) cout << " ";
        }
        cout << endl;
        cout << "save in cpp_posled.txt" << endl;
        
        return 0;
    }
    catch (const exception& e) {
        cerr << "error: " << e.what() << endl;
        return 1;
    }
}
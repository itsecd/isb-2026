#include <iostream>
#include <fstream>
#include <random>
#include <string>

using namespace std;

constexpr int BITS_AMOUNT = 128;
const char* TARGET_FILE = "number1.txt";

void write_binary(const string& filename, const string& data) {
    ofstream out(filename);
    if (!out) {
        cerr << "Error" << filename << endl;
        return;
    }
    out << data;
    out.close();
}

void generate_sequence() {
    mt19937 rng(random_device{}());
    uniform_int_distribution<int> dist(0, 1);
    string bits;
    bits.reserve(BITS_AMOUNT);
    for (int i = 0; i < BITS_AMOUNT; ++i) {
        bits += to_string(dist(rng));
    }
    write_binary(TARGET_FILE, bits);
}

int main() {
    generate_sequence();
    return 0;
}
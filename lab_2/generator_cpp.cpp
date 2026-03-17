#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <stdexcept>

using namespace std;

string generate_sequence(int length) {
    random_device rd;
    mt19937 generator(rd());
    uniform_int_distribution<int> distribution(0, 1);

    string result;
    for (int i = 0; i < length; i++) {
        result += to_string(distribution(generator));
    }
    return result;
}

void save_to_file(const string &filename, const string &sequence) {
    ofstream fout(filename);
    if (!fout) {
        throw runtime_error("Couldn't open the file to write");
    }
    fout << sequence;
    fout.close();
}

int main() {
    const int SIZE = 128;

    try {
        string sequence = generate_sequence(SIZE);
        save_to_file("cpp_sequence.txt", sequence);
        cout << "C++ sequence successfully generated" << endl;
    } catch (const exception &e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}
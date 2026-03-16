#include <iostream>
#include <fstream>
#include <cstdlib>  
#include <string>   

using namespace std;

int main() {
    srand(42);

    string binary_sequence = "";

    for (int i = 0; i < 128; i++) {
        int bit = rand() % 2;
        binary_sequence += to_string(bit);
    }

    ofstream outfile("seq_cpp.txt");
    if (outfile.is_open()) {
        outfile << binary_sequence;
        outfile.close();
        cout << "Последовательность сохранена в seq_cpp.txt" << endl;
    }
    else {
        cout << "Ошибка открытия файла!" << endl;
        return 1;
    }

    return 0;
}
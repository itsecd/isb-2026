#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

int main() {
    srand(42);
    
    const int bits_needed = 128;
    string binary_sequence = "";
    
    for (int i = 0; i < bits_needed; i++) {
        int bit = rand() % 2;
        binary_sequence += to_string(bit);
    }
    
    cout << "Сгенерированная последовательность (C++):" << endl;
    cout << binary_sequence << endl;
    
    ofstream outfile("seq_cpp.txt");
    if (outfile.is_open()) {
        outfile << binary_sequence;
        outfile.close();
        cout << "Последовательность сохранена в файл seq_cpp.txt" << endl;
    } else {
        cerr << "Ошибка открытия файла для записи" << endl;
        return 1;
    }
    
    return 0;
}
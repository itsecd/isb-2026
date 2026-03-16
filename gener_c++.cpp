#include <iostream>
#include <fstream>
#include <random>

using namespace std;

void generate_and_save(const string& filename, int length) {
    random_device rd;
    ofstream file(filename);

    for (int i = 0; i < length; i++) {
        int bit = rd() % 2;
        cout << bit;
        file << bit;
    }

    file.close();
}

int main() {
    cout << "Сгенерированная последовательность:" << "\n";
    generate_and_save("seq_cpp.txt", 128);
    return 0;
}
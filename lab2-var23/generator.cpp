#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>

using namespace std;

int main() {
    srand(24);

    string bitStream;

    for (int index = 0; index < 128; ++index) {
        bitStream += char('0' + rand() % 2);
    }

    ofstream outputFile("gen_cpp.txt");

    if (!outputFile) {
        cout << "Не удалось создать файл." << endl;
        return 1;
    }

    outputFile << bitStream;
    outputFile.close();

    cout << "Двоичная последовательность записана в gen_cpp.txt" << endl;

    return 0;
}
#include <iostream>
#include <bitset>
#include <random>
#include <fstream>
#include <string>

using namespace std;

int main() {
    //mt19937 - стандартный ГПСЧ в C++
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    // Генерируем 128 бит
    bitset<128> sequence;
    for (int i = 0; i < 128; i++) {
        sequence[i] = dis(gen);
    }

    string seq_str = sequence.to_string();

    cout << "C++ ГЕНЕРАТОР ПСЕВДОСЛУЧАЙНОЙ ПОСЛЕДОВАТЕЛЬНОСТИ" <<"\n" ;
    cout << "Генератор: mt19937 (Mersenne Twister)" << "\n";
    cout << "Длина: 128 бит" << "\n";
    cout << "Последовательность:" << "\n";
    cout << seq_str << "\n";

    // Создаем папку sequences, если её нет
    system("mkdir -p sequences");

    // Сохранение в файл
    ofstream outfile("sequence_cpp.txt");
    if (outfile.is_open()) {
        outfile << seq_str;
        outfile.close();
        cout << "Последовательность сохранена в файл: sequence_cpp.txt" << "\n";
    }
    else {
        cout << "Ошибка при сохранении в файл!" << "\n";
    }

    return 0;
}
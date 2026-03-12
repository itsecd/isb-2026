//все стикеры из сайта https://www.drive2.ru/b/2889428/
#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <locale>
#include <windows.h>
using namespace std;

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);
    SetConsoleOutputCP(CP_UTF8);
    setlocale(LC_ALL, "");
    // Определяем длину последовательности
    const int SEQUENCE_LENGTH = 128;
    // Информация о генераторе
    cout << "PSEUDORANDOM SEQUENCE GENERATOR IN C++ (mt19937)" << endl;
    cout << "Generator: mt19937 (Mersenne Twister)" << endl;
    cout << "Sequence length: " << SEQUENCE_LENGTH << " bits" << endl;
    // Открываем файл для врайтинга
    ofstream file("sequence_cpp.txt");
    if (!file.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }
    cout << "Creating file sequence_cpp.txt..." << endl;
    // Иницилизи генерейтор
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, 1);
    cout << "Starting sequence generation..." << endl;
    // Генерейтим последовательность из нулей и 1
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        file << dist(gen);
    }
    file.close();
    cout << "\nSequence saved to file: sequence_cpp.txt" << endl;
    
    ifstream check("sequence_cpp.txt");
    string line;
    check >> line;  // 
    
    // Выводить поледовательность наслаждаться результатом
    for (int i = 0; i < 128 && i < line.length(); i++) {
        cout << line[i];
        if ((i + 1) % 20 == 0) cout << " ";
        if ((i + 1) % 50 == 0 && i < 99) cout << endl;
    }
    cout << "\n------------------------------------------" << endl;
    check.close();
    // Выводить статистика
    cout << "\nSTATISTICS:" << endl;
    cout << "Total generated bits: " << line.length() << endl;
    
    // Считать нули и 1
    int zeros = 0, ones = 0;
    for (int i = 0; i < 1000 && i < line.length(); i++) {
        if (line[i] == '0') zeros++;
        else ones++;
    }
    cout << "All bits: 0 - " << zeros << ", 1 - " << ones << endl;
    cout << "Ratio 0/1: " << (float)zeros/ones << endl;
    cout << "To test, run: python nist_tests.py sequence_cpp.txt" << endl;
    return 0;
}
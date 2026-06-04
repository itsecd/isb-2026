// Генератор случайной битовой последовательности на C++
// Создаёт 128-битную последовательность с фиксированным seed и сохраняет в файл

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>

using namespace std;

int main() {
    // Устанавливаем seed для генератора случайных чисел
    srand(24);

    string bitStream;

    // Генерируем 128 случайных битов (0 или 1)
    for (int index = 0; index < 128; ++index) {
        bitStream += char('0' + rand() % 2);
    }

    // Открываем файл для записи
    ofstream outputFile("gen_cpp.txt");

    if (!outputFile) {
        cout << "Не удалось создать файл." << endl;
        return 1;
    }

    // Записываем последовательность в файл
    outputFile << bitStream;
    outputFile.close();

    cout << "Двоичная последовательность записана в gen_cpp.txt" << endl;

    return 0;
}
#include <iostream>
#include <bitset>//для работы с битовыми последовательностями
#include <random>
#include <fstream>
#include <string>

using namespace std;

int main() {
    //mt19937 - стандартный ГПСЧ в C++
    random_device rd;//Создает объект random_device - аппаратный генератор случайных чисел (используется для получения seed'а).
    mt19937 gen(rd());//Создает генератор (mt19937) и инициализирует его случайным seed'ом
    uniform_int_distribution<> dis(0, 1);//распределение от 0 до 1 

    // Генерируем 128 бит
    bitset<128> sequence;//создает битовый набор 128бит для хран последовательности
    for (int i = 0; i < 128; i++) {
        sequence[i] = dis(gen);//заполняем последовательность случ.числом 0 и 1
    }

    string seq_str = sequence.to_string();//преобразуем битовую последовательность в строку



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
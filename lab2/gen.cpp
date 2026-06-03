#include <iostream>
#include <fstream>
#include <random>
#include <ctime>

using namespace std;

void generate()
{
    try
    {
        ofstream file("cpp_sequence.txt");

        if (!file)
        {
            throw runtime_error("Не удалось открыть файл");
        }

        mt19937 gen(time(nullptr));
        uniform_int_distribution<int> dist(0, 1);

        for (int i = 0; i < 128; i++)
        {
            file << dist(gen);
        }

        file.close();

        cout << "C++: файл успешно создан" << endl;
    }
    catch (const exception &e)
    {
        cout << "Ошибка C++ генерации: " << e.what() << endl;
    }
}

int main()
{
    generate();
    return 0;
}

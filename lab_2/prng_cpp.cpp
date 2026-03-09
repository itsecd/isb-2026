#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

void generate_string()
{
    srand(time(NULL));
    std::ofstream file("cpp_string.txt");
    if (file.is_open())
    {
        for (int i = 0; i < 128; i++)
        {
            int random_bit = rand() % 2;
            file << random_bit;
        }
    }
    else
    {
        std::cout << "Не удалось сгенерировать последовательность, увы(";
    }
}

int main()
{
    generate_string();
}
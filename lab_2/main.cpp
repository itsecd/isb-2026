#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

void generate_random_num()
{
    srand(time(NULL));
    std::ofstream file("output_cpp.txt");
    if (file.is_open())
    {
        for (int i = 0; i < 128; i++)
        {
            int random_num = rand() % 2;
            file << random_num;
        }
    }
    else
    {
        std::cout << "Не удалось сгенерировать число!";
    }
}

int main()
{
}
#include <random>
#include <fstream>

int main()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);

    std::ofstream file("result_cpp.txt");
    if (file)
    {
        for (int i = 0; i < 128; i++)
        {
            file << std::to_string(dist(gen));
        }
    }
    file.close();
}
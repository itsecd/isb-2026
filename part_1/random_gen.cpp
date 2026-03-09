#include <fstream>
#include <cstdlib>
#include <ctime>
#include <vector>

std::vector<int> random_gen()
{
    std::vector<int> data;
    srand(time(NULL));
    for (int i = 0; i < 128; i++)
    {
        int random = rand() % 2;
        data.push_back(random);
    }
    return data;
}

void save_data(std::vector<int> data)
{
    std::ofstream os;
    os.open("c_gen.txt");
    if (os.is_open())
    {
        for (size_t i = 0; i < data.size(); ++i)
        {
            os << data[i];
        }
    }
    os.close();
}

int main()
{
    std::vector<int> generated = random_gen();
    save_data(generated);
}
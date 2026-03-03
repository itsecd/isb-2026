#include <fstream>
#include <iostream>
#include <random>

using namespace std;

int main()
{

    ofstream fout;
    fout.open("cpp.txt");

    random_device eng;
    uniform_int_distribution<int> dist(0, 1);

    for (size_t i = 0; i < 128; i++)
    {
        fout << (dist(eng) == 0) ? 0 : 1;
    }

    fout.close();

    return 0;
}
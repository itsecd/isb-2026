#include <cstddef>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

constexpr size_t BIT = 128;
constexpr char FILENAME[] = "bits_cpp.txt";

void writeBitsToFile(const string &filename, const vector<int> bits)
{
    ofstream file(filename);
    if (!file.is_open())
    {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    for (size_t i = 0; i < bits.size(); ++i)
    {
        file << bits[i];
    }
}

void generator(vector<int> &bits)
{
    for (size_t i = 0; i < BIT; ++i)
    {
        int buf = rand() % 2;
        bits.push_back(buf);
    }
    writeBitsToFile(FILENAME, bits);
}

int main()
{
    srand(time(nullptr));
    vector<int> bits;
    generator(bits);
}

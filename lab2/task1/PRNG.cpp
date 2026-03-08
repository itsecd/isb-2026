#include <random>
#include <string>
#include <fstream>

void generate_random_sequence(const std::string &path)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    std::string seq;
    for (int i = 0; i < 128; ++i)
        seq += std::to_string(dis(gen));
    std::ofstream file(path);
    file << seq;
}

int main()
{
    generate_random_sequence("seq_generator_cpp.txt");
}
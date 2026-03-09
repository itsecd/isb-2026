#include <fstream>
#include <random>

int main()
{
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dis(0, 1);

    std::ofstream out("cpp_seq.txt");

    for (int i = 0; i < 128; ++i) {
        out << dis(gen);
    }

    out.close();
    return 0;
}


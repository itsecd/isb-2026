#include <iostream>
#include <fstream>
#include "generator.h"

int main()
{
    const size_t N = 128;

    std::string sequence = generateSequence(N);

    std::ofstream out("results.txt");
    out << sequence << "\n\n";


    out.close();

    std::cout << "Results saved to results.txt\n";

    return 0;
}
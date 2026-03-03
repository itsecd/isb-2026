#include <iostream>
#include <fstream>
#include "generator.h"
#include "nist_tests.h"

int main()
{
    const size_t N = 128;

    std::string sequence = generateSequence(N);

    double p1 = frequencyTest(sequence);
    double p2 = runsTest(sequence);
    double p3 = longestRunTest(sequence);

    std::ofstream out("results.txt");

    out << "Generated sequence (128 bits):\n";
    out << sequence << "\n\n";

    out << "===== NIST TEST RESULTS =====\n";
    out << "Frequency Test P-value: " << p1;
    out << (p1 >= 0.01 ? " (PASS)\n" : " (FAIL)\n");

    out << "Runs Test P-value: " << p2;
    out << (p2 >= 0.01 ? " (PASS)\n" : " (FAIL)\n");

    out << "Longest Run Test P-value: " << p3;
    out << (p3 >= 0.01 ? " (PASS)\n" : " (FAIL)\n");

    out.close();

    std::cout << "Results saved to results.txt\n";

    return 0;
}
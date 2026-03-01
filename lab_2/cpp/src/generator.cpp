#include "generator.h"
#include <random>

std::string generateSequence(size_t length)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);

    std::string sequence;
    sequence.reserve(length);

    for (size_t i = 0; i < length; ++i)
        sequence += std::to_string(dist(gen));

    return sequence;
}
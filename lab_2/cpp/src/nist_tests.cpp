#include "nist_tests.h"
#include <cmath>
#include <vector>

double frequencyTest(const std::string& seq)
{
    int sum = 0;
    for (char c : seq)
        sum += (c == '1') ? 1 : -1;

    double s_obs = std::abs(sum) / std::sqrt(seq.size());
    return std::erfc(s_obs / std::sqrt(2.0));
}

double runsTest(const std::string& seq)
{
    int N = seq.size();
    int ones = 0;

    for (char c : seq)
        if (c == '1')
            ones++;

    double pi = static_cast<double>(ones) / N;

    if (std::abs(pi - 0.5) >= (2.0 / std::sqrt(N)))
        return 0.0;

    int Vn = 1;
    for (int i = 1; i < N; ++i)
        if (seq[i] != seq[i - 1])
            Vn++;

    double numerator = std::abs(Vn - 2 * N * pi * (1 - pi));
    double denominator = 2 * std::sqrt(2 * N) * pi * (1 - pi);

    return std::erfc(numerator / denominator);
}

double longestRunTest(const std::string& seq)
{
    const int M = 8;
    const int blocks = seq.size() / M;

    int count[4] = { 0 };

    for (int i = 0; i < blocks; ++i)
    {
        int maxRun = 0;
        int currentRun = 0;

        for (int j = 0; j < M; ++j)
        {
            if (seq[i * M + j] == '1')
            {
                currentRun++;
                maxRun = std::max(maxRun, currentRun);
            }
            else
                currentRun = 0;
        }

        if (maxRun <= 1) count[0]++;
        else if (maxRun == 2) count[1]++;
        else if (maxRun == 3) count[2]++;
        else count[3]++;
    }

    double pi[4] = { 0.2148, 0.3672, 0.2305, 0.1875 };
    double chi2 = 0.0;

    for (int i = 0; i < 4; ++i)
    {
        double expected = blocks * pi[i];
        chi2 += (count[i] - expected) * (count[i] - expected) / expected;
    }

    return std::exp(-chi2 / 2.0);
}
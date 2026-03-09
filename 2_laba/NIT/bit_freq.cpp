#include <cmath>
#include <vector>
#include "h/bit_freq.h"

double bitFrequencyTest(int n, const std::vector<int> &req)
{
  double X = 0;
  for (int elem : req)
  {
    X += (elem == 1) ? 1 : -1;
  }
  double S = X / std::sqrt(n);
  return std::erfc(std::fabs(S) / std::sqrt(2.0));
}
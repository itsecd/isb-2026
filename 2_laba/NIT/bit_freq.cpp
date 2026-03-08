#include <cmath>
#include <vector>
#include "h/bit_freq.h"

double bitFrequencyTest(const int n, const std::vector<int> &req)
{
  int X = 0;
  for (auto elem : req)
    elem == 1 ? X += 1 : X -= 1;
  auto S = X / sqrt(n);
  return erfc(S / sqrt(2));
}

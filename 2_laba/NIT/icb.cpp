#include <cmath>
#include <vector>
#include "h/icb.h"

double identicalConsecutiveBitsTest(const int n, const std::vector<int>& req)
{
  double eps = 0;
  for (auto elem : req)
    eps += elem;
  double dzeta = eps / n;

  if (std::fabs(dzeta - 0.5) >= 2.0 / std::sqrt(n))
    return 0.0;

  int V = 0;
  for (int i = 0; i < n - 1; ++i)
    if (req[i] != req[i + 1])
      V += 1;

  return erfc(fabs(V - 2 * n * dzeta * (1 - dzeta)) / (2 * sqrt(2 * n) * dzeta * (1 - dzeta)));
}
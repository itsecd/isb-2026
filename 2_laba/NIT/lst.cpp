#include <cmath>
#include <vector>
#include <boost/math/special_functions/gamma.hpp>
#include "h/lst.h"

double longestSequenceOneTest(const int n, const std::vector<int> seq, const std::vector<double> &pi)
{
  int M = 8;
  int countBlock = n / M;

  std::vector<int> v(4, 0);

  for (int i = 0; i < countBlock; ++i)
  {
    int max = 0;
    int cur = 0;

    for (int j = 0; j < M; ++j)
    {
      if (!seq[M * i + j])
        cur = 0;
      else
      {
        ++cur;
        if (cur > max)
          max = cur;
      }
    }

    if (max <= 1)
      v[0]++;
    else if (max == 2)
      v[1]++;
    else if (max == 3)
      v[2]++;
    else
      v[3]++;
  }

  double X = 0.0;
  for (int i = 0; i < 4; ++i)
    X += pow(v[i] - 16 * pi[i], 2) / (16 * pi[i]);

  return boost::math::gamma_q(1.5, X / 2);
}
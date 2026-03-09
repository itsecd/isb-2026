#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

#include "h/bit_freq.h"
#include "h/icb.h"
#include "h/lst.h"
#include "h/util.h"
#include "h/constants.h"

void process(const std::string &path, std::vector<int> vec, const std::string &result, const std::string &name)
{
  read(path, vec);

  double p_freq = bitFrequencyTest(N, vec);
  double p_icb = identicalConsecutiveBitsTest(N, vec);
  double p_lsb = longestSequenceOneTest(N, vec, pi);

  write(result, name, p_freq, p_icb, p_lsb);
}

int main()
{
  std::string path_out, path_inp;
  std::vector<int> vec;

  std::cout << "Enter file name 1 (e.g., ../generate/generate_cpp.txt): ";
  std::cin >> path_inp;
  std::cout << "Enter file name for recording: ";
  std::cin >> path_out;

  process(path_inp, vec, path_out, "C++");

  std::cout << "Enter file name 2 (e.g., ../generate/generate_java.txt): ";
  std::cin >> path_inp;

  process(path_inp, vec, path_out, "Java");

  std::cout << "Enter file name 3 (e.g., ../generate/generate_c.txt): ";
  std::cin >> path_inp;

  process(path_inp, vec, path_out, "C");
}
#include <vector>
#include <string>
#include <fstream>
#include <stdexcept>
#include "h/util.h"

void read(const std::string &path, std::vector<int> &vec)
{
  std::ifstream file(path);
  if (!file.is_open())
    throw std::runtime_error("the file did not open");
  char elem = ' ';
  while (file.get(elem))
  {
    if (elem == '0' || elem == '1')
      vec.push_back(elem - '0');
  }
}

void write(const std::string &filename, const std::string &name, double p_freq, double p_icb, double p_lsb)
{
  std::ofstream out(filename, std::ios::app);
  out << name << std::endl;
  out << "frequency test:               P = " << p_freq
      << " -> " << (p_freq >= 0.01 ? "true" : "false") << std::endl;
  out << "test for consecutive bits:   P = " << p_icb
      << " -> " << (p_icb >= 0.01 ? "true" : "false") << std::endl;
  out << "Longest Run Test:           P = " << p_lsb
      << " -> " << (p_lsb >= 0.01 ? "true" : "false") << std::endl
      << std::endl;
  out.close();
}

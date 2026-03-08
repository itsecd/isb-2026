#include <iostream>
#include <random>
#include <fstream>
#include <vector>
#include <string>

std::vector<int> minstd(int seed, size_t n)
{
  std::minstd_rand mr(seed);
  std::vector<int> result;

  while (result.size() < n)
  {
    auto key = mr();
    for (int i = 0; i < 31 && result.size() < n; ++i)
      result.push_back((key >> i) & 1);
  }

  return result;
}

void write(const std::string& path, const std::vector<int>& req)
{
  std::ofstream output(path);
  for (auto elem : req)
    output << elem;
}

int main()
{
  size_t n = 128;
  int seed = 11342;

  auto result = minstd(seed, n);

  std::string path = "generate_cpp.txt";

  write(path, result);
}
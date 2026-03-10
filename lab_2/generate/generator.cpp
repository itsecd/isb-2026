#include <iostream>
#include <random>
#include <string>

int main() {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> dis(0, 1);

  std::string sequence = "";
  for (int i = 0; i < 128; ++i) {
    sequence += std::to_string(dis(gen));
  }

  std::cout << "Sequence: " << sequence << std::endl;
  return 0;
}

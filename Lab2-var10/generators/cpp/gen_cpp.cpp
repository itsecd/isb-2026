#include <iostream>
#include <fstream>
#include <random>
#include <chrono>

const int N = 128;  

int main() {
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 gen(seed);
    std::uniform_int_distribution<int> dist(0, 1);

    std::ofstream f("../../sequences/seq_cpp.txt");
    if (!f.is_open()) {
        std::cerr << "Failed to open file" << std::endl;
        return 1;
    }

    for (int i = 0; i < N; ++i) {
        f << dist(gen);
    }
    f.close();
    return 0;
}

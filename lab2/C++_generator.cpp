#include <fstream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());  
    std::uniform_int_distribution<int> dist(0, 1);

    std::ofstream f("C++.txt");
    for (int i = 0; i < 128; i++) {  
        f << dist(gen);
    }
    return 0;
}

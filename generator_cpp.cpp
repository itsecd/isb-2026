#include <fstream>
#include <cstdlib>
#include <ctime>

int main() {
    std::srand(std::time(nullptr));
    std::ofstream out("sequence_cpp.txt");
    for (int i = 0; i < 128; ++i) {
        out << (std::rand() % 2);
    }
    out << std::endl;
    return 0;
}
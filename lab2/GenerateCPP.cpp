#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));

    std::cout << "C++ Generated Sequence (128 bits):" << std::endl;
    for (int i = 0; i < 128; ++i) {
        std::cout << (rand() % 2);
    }
    std::cout << std::endl;
    return 0;
}

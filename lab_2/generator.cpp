#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int main(int argc, char* argv[]) {
    unsigned int seed = 12345;
    srand(seed);

    const int N = 128;

    std::ostream* out = &std::cout;
    std::ofstream file;
    if (argc > 1) {
        file.open(argv[1]);
        if (!file.is_open()) {
            std::cerr << "Не удалось открыть файл для записи: " << argv[1] << std::endl;
            return 1;
        }
        out = &file;
    }

    for (int i = 0; i < N; ++i) {
        int bit = rand() % 2;         
        *out << bit;
    }
    *out << std::endl;

    if (file.is_open()) file.close();
    return 0;
}
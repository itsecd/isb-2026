#include <iostream>
#include <fstream>
#include <random>

int main() {
    const long N = 1000000;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);

    std::ofstream out("sequences/sequence_cpp.txt");
    if (!out.is_open()) {
        std::cerr << "Ошибка создания файла!\n";
        return 1;
    }
    for (long i = 0; i < N; ++i)
        out << dist(gen);
    out.close();
    std::cout << "Готово! " << N << " бит сохранено в sequences/sequence_cpp.txt\n";
    return 0;
}
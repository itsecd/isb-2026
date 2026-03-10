#include <fstream>
#include <random>

const std::string FILE_PATH = "lab_2/sequences/cpp_seq.txt";
const size_t SIZE = 128;

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution dist(0, 1);

    std::ofstream file(FILE_PATH);
    if (!file.is_open()) {
        throw "Ошибка при создании файла!";
    }

    for (size_t i = 0; i < SIZE; i++) {
        file << dist(gen);
    }

    file.close();
    return 0;
}
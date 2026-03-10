#include <fstream>
#include <random>

int main() {

    const int LENGTH = 128;

    std::ofstream output("seq_cpp.txt");

    if (!output.is_open()) {
        return 1;
    }

    std::random_device device;
    std::mt19937 engine(device());
    std::uniform_int_distribution<int> bit(0, 1);

    for (int i = 0; i < LENGTH; ++i) {
        int value = bit(engine);
        output << value;
    }

    return 0;
}

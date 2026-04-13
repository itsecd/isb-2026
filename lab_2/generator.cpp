#include <string>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));

    for (int j = 1; j <= 3; j++) {

        std::string filename = "sequence" + std::to_string(j) + ".txt";
        std::ofstream file(filename);

        for (int i = 0; i < 128; i++) {
            int bit = rand() % 2;
            file << bit;
        }

        file.close();
    }

    std::cout << "3 sequences generated and saved." << std::endl;

    return 0;
}
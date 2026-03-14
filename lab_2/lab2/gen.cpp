#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {
    ofstream out("seq_cpp.txt");
    srand(time(0));

    int n = 128;

    for (int i = 0; i < n; i++) {
        out << rand() % 2;
    }

    out.close();
    return 0;
}

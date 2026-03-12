#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {

    srand(time(0));

    for (int i = 0; i < 128; i++) {
        cout << rand() % 2;
    }

    cout << endl;

    return 0;
}
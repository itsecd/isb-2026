#include <fstream>
#include <random>

using namespace std;

int main(){
    random_device en;
    uniform_int_distribution d(0, 1);

    ofstream f;
    f.open("C++.txt");
    for(int i=0; i<128; i++){
        f << d(en);
    }
    f.close();

    return 0;
}

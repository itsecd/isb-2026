#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib> 
#include <ctime>

using namespace std;

void write_data(vector<int> vec, string filename) {
    ofstream file(filename);
    for(int i = 0; i < 128; i++) {
        file << vec[i];
    }
}

void generator(string filename) {
    vector<int> vec;
    for (int i = 0; i < 128; i++) {
        vec.push_back(rand() % 2);
    }
    write_data(vec, filename);
}

int main()
{
    srand(time(NULL));
    string filename;
    cout << "Input name for file output:";
    cin >> filename;
    generator(filename);
}
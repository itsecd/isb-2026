#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>

using namespace std;

vector<long long> readConstants() {
    vector<long long> values;
    ifstream file("constants.txt");
    string line;
    while (getline(file, line)) {
        size_t comment = line.find('#');
        if (comment != string::npos) line = line.substr(0, comment);
        line.erase(0, line.find_first_not_of(" \t"));
        line.erase(line.find_last_not_of(" \t") + 1);
        if (!line.empty()) values.push_back(stoll(line));
    }
    file.close();
    return values;
}

int main() {
    vector<long long> vals = readConstants();
    int LENGTH = (int)vals[0];
    
    srand(time(nullptr));
    
    string bits;
    for (int i = 0; i < LENGTH; i++) {
        bits += (rand() % 2) ? '1' : '0';
    }
    
    system("mkdir results 2>nul");
	
    ofstream out("results/sequence_cpp.txt");
    out << bits;
    out.close();
    
    return 0;
}
#include "filereading.h"
#include <fstream>
#include <string>
using namespace std;


string read_file(const char* path) {
    ifstream file(path);
    if (!file.is_open()) {
        throw std::invalid_argument("Uncorrect path or file!");
    }
    string res;
    getline(file, res);
    return res;
}
std::vector<int> read_vector(const string& line) {
    std::vector<int> result;
    for (auto u : line) {
        if (u == '0') {
            result.push_back(0);
        }
        else if (u == '1') {
            result.push_back(1);
        }
        else {
            throw std::runtime_error("Uncorrect file format!");
        }
    }
    return result;
}

std::vector<int> read_sequence(const char* path) {
    return read_vector(read_file(path));
}
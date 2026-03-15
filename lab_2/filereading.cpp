#include "filereading.h"

using namespace std;

std::vector<int> read_vector(const char* line) {
    std::vector<int> result;

    const char* p = line;
    while (*p != '\0') {
        if (*p == '0') {
            result.push_back(0);
        }
        else if (*p == '1') {
            result.push_back(1);
        }
        p++;
    }
    return result;
}
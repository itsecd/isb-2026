#ifndef FILEREADING_H
#define FILEREADING_H

#include <vector>

char* read_row(const char* path);

std::vector<int> read_vector(const char* line);

#endif
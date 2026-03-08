#ifndef UTIL_H
#define UTIL_H

#include <vector>
#include <string>

void read(const std::string &path, std::vector<int> &vec);
void write(const std::string &filename, const std::string &name, double p_freq, double p_icb, double p_lsb);

#endif
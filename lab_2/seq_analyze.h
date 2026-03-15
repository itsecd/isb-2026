#ifndef SEQ_ANALYSIS_H
#define SEQ_ANALYSIS_H

#include <iostream>
#include <vector>

double freq_p_value(const std::vector<int>& seq);
double repeat_p_value(const std::vector<int>& seq);
double block_hi_squared(const std::vector<int>& seq);
#endif
#ifndef SEQ_ANALYSIS_H
#define SEQ_ANALYSIS_H

#include <iostream>
#include <vector>

int psi(int omega);

int psi_sum(const std::vector<int>& seq);

double freq_p_value(const std::vector<int>& seq);
#endif
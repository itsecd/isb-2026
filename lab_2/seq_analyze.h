#ifndef SEQ_ANALYSIS_H
#define SEQ_ANALYSIS_H

#include <iostream>
#include <vector>


double freq_p_value(const std::vector<int>& seq);
double repeat_p_value(const std::vector<int>& seq);
double seq_hi_squared(const std::vector<int>& seq);

void seq_statistics(const std::vector<int>& seq, std::ostream& os);
#endif
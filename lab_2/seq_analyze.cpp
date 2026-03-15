#include "seq_analyze.h"
#include <cmath>

int psi(int omega) {
	if (omega == 1) {
		return 1;
	}
	else if (omega == 0) {
		return -1;
	}
	else {
		throw std::invalid_argument("omega must be 0 or 1");
	}
}

int psi_sum(const std::vector<int>& seq) {
	int res = 0;
	for (auto u : seq) {
		res += psi(u);
	}
	return res;
}

double freq_p_value(const std::vector<int>& seq) {
	return erfc(psi_sum(seq) / (sqrt(2)));
}
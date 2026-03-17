#include "seq_analyze.h"
#include <cmath>

using namespace std;

//��������� ����
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
	return res/sqrt(seq.size());
}

double freq_p_value(const std::vector<int>& seq) {
	return erfc(psi_sum(seq) / (sqrt(2)));
}

//���� �� ������������� ��������
double zeta(const std::vector<int>& seq) {
	double res = 0;
	for (auto u : seq) {
		res += u;
	}
	return res / seq.size();
}

int V_N(const std::vector<int>& seq) {
	int res = 0;
	for (size_t i = 0; i < seq.size() - 1; i++) {
		if (seq[i] != seq[i + 1]) {
			res += 1;
		}
	}
	return res;
}

double repeat_p_value(const std::vector<int>& seq) {
	double zta = zeta(seq);
	if (abs(zta - 1 / 2) >= 2 / sqrt(seq.size())) {
		return 0;
	}
	int Vn = V_N(seq);

	return erfc(abs(Vn - 2 * (int)seq.size() * zta * (1 - zta)) / (2 * sqrt(2 * (int)seq.size()) * zta * (1 - zta)));
}

//���� �� ����� ������� ������������������ ������ � �����
size_t block(const vector<int>& seq, size_t start, size_t block_size) {
	size_t i = start;
	size_t res = 0;
	while (i < start + block_size) {
		size_t tmp = 0;
		while (i < start + block_size && seq[i] == 1) {
			++tmp;
			++i;
		}
		if (tmp > res) {
			res = tmp;
		}
		++i;
	}
	return res;
}

vector<int> V(const vector<int>& seq) {
	vector<int> res(4);
	for (size_t i = 0; i < seq.size(); i += 8) {
		size_t bl = block(seq, i, 8);
		if (bl <= 1) {
			res[0]++;
		}
		else if (bl == 2) {
			res[1]++;
		}
		else if (bl == 3) {
			res[2]++;
		}
		else {
			res[3]++;
		}
	}
	return res;
}


double seq_hi_squared(const std::vector<int>& seq) {
	double pi[4] = { 0.2148,0.3672,0.2305,0.1875 };

	vector<int> V_vect = V(seq);

	double hi_squared = 0;
	for (size_t i = 0; i < 4; ++i) {
		double tmp = (V_vect[i] - 16 * pi[i]);
		hi_squared += tmp * tmp / (16 * pi[i]);
	}
	
	return hi_squared;
}

void seq_statistics(const std::vector<int>& seq, ostream& os) {
	os << "_________________________________________\n";
	os << "frequency analysis p_value = " << freq_p_value(seq) << '\n';
	os << "repeating analysis p_value = " << repeat_p_value(seq) << '\n';
	os << "hi-square of vector = " << seq_hi_squared(seq) << '\n';
	os << "_________________________________________\n";
}
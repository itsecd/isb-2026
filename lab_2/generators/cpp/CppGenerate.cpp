#include "CppGenerate.h"

#include <cstdlib>
#include <ctime> 
#include <fstream>

using namespace std;


int generateDRV() {
	srand(time(nullptr));
	float q = rand();
	if (q >= 0.5) {
		return 1;
	}
	return 0;
}


vector<int> generateDRVec() {
	vector<int> result(128);
	for (int i = 0; i < 128; i++) {
		result[i] = generateDRV();
	}
	return result;
}


void write_file(const char* path) {
	ofstream outputFile(path);

	if (!outputFile.is_open()) {
		cerr << "Ошибка открытия файла для записи!";
		throw std::invalid_argument("Uncorrect file path!");
	}

	for (size_t i = 1; i < 128; ++i) {
		vector<int> DRVec = generateDRV();
		for (auto u : DRVec) {
			outputFile << u;
		}
		outputFile << "\n";
	}
}
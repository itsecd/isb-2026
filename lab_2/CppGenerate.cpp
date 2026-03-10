#include <iostream>
#include <cstdlib>  // для rand(), srand()
#include <ctime>   // для time()
#include <vector>

using namespace std;

int generateDRV() {
	srand(static_cast<unsigned int>(std::time(nullptr)));
	float q = rand();
	if (q >= 0.5) {
		return true;
	}
	return false;
}


vector<int> generateDRVec() {
	vector<int> result(128);
	for (int i = 0; i < 128; i++) {
		result[i] = generateDRV();
	}
	return result;
}
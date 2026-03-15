#include <iostream>
#include "generators/cpp/CppGenerate.h"
#include "seq_analyze.h"
#include "filereading.h"

using namespace std;

int main() {
	// write_file("E:\\working\\inform-security-base\\inform-security-base\\lab_2\\generators\\cpp\\gen.txt",1000);
	vector<int> seq = read_vector("100101");
	cout << seq[3];
	return 0;
}
#include <iostream>
#include <random>
#include <fstream>

using namespace std;


int main() {
	ofstream f("out_cpp.txt");
	random_device rd;
	mt19937 gen(rd());
	uniform_int_distribution<> dist(0, 1);
	for (int i = 0; i < 128; ++i) {
		f << dist(gen);
	}
	return 0;
}
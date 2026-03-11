#include <iostream>
#include <random>
#include <string>
#include <fstream>

using namespace std;

mt19937 gen(random_device{}());
uniform_int_distribution<> dist(0, 1);

int generate_bit() {
	return dist(gen);
}


void write_sequences_into_file(int size) {
	ofstream file("../../../../sequences/sequence_cpp.txt");
	if (!file.is_open()) {
		cerr << "Error to open: ../sequences/sequence_cpp.txt" << '\n';
		return;
	}
	for (int i = 0; i < size; ++i) {
		file << generate_bit();
	}
	file.close();
	cout << "ok" << '\n';
}


int main() {
	write_sequences_into_file(128);
	return 0;

}

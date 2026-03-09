#include<iostream>
#include<fstream>
#include<random>
using namespace std;

int main() {
	ofstream file;
	file.open("seq_c.txt");
	random_device eng;
	uniform_int_distribution<int> dist(0, 1);
	for (int i = 0; i < 128; i++) {
		file << dist(eng); 
	}
	file.close();
}
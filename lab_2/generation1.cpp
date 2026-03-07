#include<iostream>
#include<fstream>
#include<cstdlib>
#include<ctime>
#include<string>

#define SIZE 128

int main() {
	std::string seq = "";
	srand(time(NULL));
	for (int i = 0; i < SIZE; i++) {
		seq += char('0' + rand() % 2);
	}
	std::cout << "Generated sequence (C++):\n" << seq << "\n";
	std::ofstream fout("seq_cpp.txt");
	fout << seq;
	fout.close();
	return 0;
}
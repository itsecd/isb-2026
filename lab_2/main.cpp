#include <iostream>
#include <fstream>
#include "generators/cpp/CppGenerate.h"
#include "seq_analyze.h"
#include "filereading.h"

using namespace std;

int main() {
	//write_file("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt",1);
	
	ofstream stats_file("D:\\UniversityLabs\\inform-security-base\\lab_2\\statistics.txt");


	// Читаем сначала С++ вектор
	stats_file << "C++ generated vector\n";
	vector<int> cpp_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt");
	seq_statistics(cpp_vec,stats_file);

	// Java вектор
	stats_file << "Java generated vector\n";
	vector<int> java_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\java\\JavaGenerated.txt");
	seq_statistics(java_vec,stats_file);

	// Java вектор
	stats_file << "Python generated vector\n";
	vector<int> python_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\python\\PyGen.txt");
	seq_statistics(python_vec,stats_file);
}
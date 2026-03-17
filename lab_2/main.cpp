#include <iostream>
#include "generators/cpp/CppGenerate.h"
#include "seq_analyze.h"
#include "filereading.h"

using namespace std;

int main() {
	//write_file("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt",1);
	
	// Читаем сначала С++ вектор
	cout << "C++ generated vector\n";
	vector<int> cpp_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt");
	seq_statistics(cpp_vec,cout);

	// Java вектор
	cout << "Java generated vector\n";
	vector<int> java_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\java\\JavaGenerated.txt");
	seq_statistics(java_vec,cout);

	// Java вектор
	cout << "Python generated vector\n";
	vector<int> python_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\python\\PyGen.txt");
	seq_statistics(python_vec,cout);
}
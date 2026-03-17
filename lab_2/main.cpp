#include <iostream>
#include "generators/cpp/CppGenerate.h"
#include "seq_analyze.h"
#include "filereading.h"

using namespace std;

int main() {
	//write_file("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt",1);
	
	// Читаем сначала С++ вектор
	vector<int> cpp_vec = read_sequence("D:\\UniversityLabs\\inform-security-base\\lab_2\\generators\\cpp\\CppGen.txt");
	
}
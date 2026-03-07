#include <cstdlib>
#include<vector>
#include<fstream>
#include<ctime>



void write_file(std::string filename,std::vector<int>data) {
	std::ofstream os(filename);

	if (!os.is_open()) { 
		return; 
	}
	for (int i = 0; i < data.size(); i++) {
		os << data[i];
	}
	os.close();
}

void generator(std::string filename) {
	std::vector<int>data;
	srand(time(NULL));
	for (int i = 0; i < 128; i++) {
		int random = rand() % 2;
		data.push_back(random);
	}
	write_file(filename, data);
}
int main() {
	 std::string filename = "C:\\Users\\Honor\\Desktop\\isb-2026\\lab_2\\output_c.txt";
	 generator(filename);

}



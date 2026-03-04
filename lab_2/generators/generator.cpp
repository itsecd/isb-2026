#include <fstream>
#include <random>
#include <vector>
#include <string>
#include <iostream>  

std::vector<int> gen_bits(const size_t size){//генерация послеовательности битов
    std::vector<int> res(size);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(0, 1);

    for(auto &i : res){
        i = dist(gen);
    }
    return res;
}

template <typename T>
std::ostream& operator <<(std::ostream& os, const std::vector<T>& vec){//вывод вектора
    for(auto &i : vec){
        os << i;
    }
    return os;
}

template <typename T>
void file_writter(const std::string filename, const std::vector<T>& vec){//запись в файл
    std::ofstream out(filename);
    if(out.is_open()){
        out << vec;
    }
    else{
        std::cerr << "Error with open file." << std::endl;
    }
}

int main(int argc, char* argv[]){
    int count = argc > 1? std::stoi(argv[1]) : 128;
    if (count <= 0 ) count = 128;
    const std::string filename = argc > 2 ? argv[2] : "../../lab_2/gen_bits/cpp_gen.txt";
    file_writter(filename, gen_bits(count));
}
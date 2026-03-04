#include <random>
#include <string>
#include <iostream>
#include <fstream> 
#include "config.hpp"

std::string generator(){
    std::string result = "";
    result.reserve(128);

    std::random_device rd;
    std::mt19937 gen(rd());
    
    std::uniform_int_distribution<int> dis(0, 1);

    for(int i = 0; i < 128; i++){
        int rand = dis(gen);
        result += std::to_string(rand);
    }
    return result;
}

void save_to_file(std::string text, std::string path){
    std::ofstream out(path); 
    if (out.is_open()) {
   
        out << text << std::endl;
        out.close(); 

    } else {
        std::cerr << "Ошибка при открытии файла!" << std::endl;
    }

}

int main(){
    std::string res = generator();
    save_to_file(res, Config::FILE_PATH);
}
#include <iostream>
#include <random>
#include <fstream>
#include <string>
#include <chrono>

class RandomGenerator {
public:
    std::string generateMT19937(int length) {
        std::mt19937 gen(std::random_device{}());
        std::uniform_int_distribution<> dist(0, 1);
        
        std::string sequence;
        for (int i = 0; i < length; ++i) {
            sequence += std::to_string(dist(gen));
        }
        return sequence;
    }
    
    std::string generateMinstd(int length) {
        std::minstd_rand gen(std::chrono::system_clock::now().time_since_epoch().count());
        std::uniform_int_distribution<> dist(0, 1);
        
        std::string sequence;
        for (int i = 0; i < length; ++i) {
            sequence += std::to_string(dist(gen));
        }
        return sequence;
    }
    
    std::string generateDefault(int length) {
        std::default_random_engine gen(std::random_device{}());
        std::uniform_int_distribution<> dist(0, 1);
        
        std::string sequence;
        for (int i = 0; i < length; ++i) {
            sequence += std::to_string(dist(gen));
        }
        return sequence;
    }
};

int main() {
    RandomGenerator generator;
    int length = 128;
    
    std::string seq1 = generator.generateMT19937(length);
    std::string seq2 = generator.generateMinstd(length);
    std::string seq3 = generator.generateDefault(length);
    
    std::ofstream file("sequences_cpp.txt");
    file << "Sequence 1 (MT19937):\n" << seq1 << "\n\n";
    file << "Sequence 2 (minstd_rand):\n" << seq2 << "\n\n";
    file << "Sequence 3 (default_random_engine):\n" << seq3 << "\n";
    file.close();
    
    std::cout << "Sequences generated and saved to sequences_cpp.txt\n";
    std::cout << "Sequence 1: " << seq1 << "\n";
    std::cout << "Sequence 2: " << seq2 << "\n";
    std::cout << "Sequence 3: " << seq3 << "\n";
    
    return 0;
}
#include <fstream>
#include <cstdint>

int main() {
    std::ofstream fout("C++.txt");
    
    uint32_t state = 12345;  // начальное значение (seed)
    
    for (int i = 0; i < 128; i++) {
        // Линейный конгруэнтный генератор
        state = (1103515245 * state + 12345) % 2147483648;
        
        // Берем младший бит
        int bit = state & 1;
        
        fout << bit;
    }
    
    fout.close();
    return 0;
}
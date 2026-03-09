//Ну вот почему в с++ сохраниение файлов нормально работает только с танцами с бубном и жертвоприношениями...

#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <string>
#include <filesystem>
using namespace std;
namespace fs = std::filesystem;

void num_gen(vector<int>& numbers)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, 1);

    for (int i = 0; i < numbers.size(); i++)
    {
        numbers[i] = dist(gen);
    }
}

void save_to_file(const vector<int>& numbers, const string& filename)
{
    fs::path file_path(filename);
    fs::path dir = file_path.parent_path();

    if (!dir.empty() && !fs::exists(dir)) {
        fs::create_directories(dir);
        cout << "Создана директория: " << dir << endl;
    }

    ofstream file(filename);
    if (file.is_open()) {
        for (int num : numbers)
        {
            file << num;
        }
        file.close();
        cout << "Последовательность сохранена в файл: " << filename << endl;
    }
    else {
        cout << "Ошибка при открытии файла: " << filename << endl;
    }
}

int main() {
#if _MSC_VER
    system("chcp 65001 > nul");
#endif
    ios_base::sync_with_stdio(false);

    vector<int> numbers(128, 0);

    num_gen(numbers);

    
    string source_dir = SOURCE_DIR;  
    fs::path lab2_path = fs::path(source_dir).parent_path();  
    string filename = (lab2_path / "task2" / "sequence_c++.txt").string();

    save_to_file(numbers, filename);

    return 0;
}
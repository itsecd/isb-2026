#include <iostream>
#include <string>
#include <random>
#include <cmath>
#include <fstream>
#include <filesystem>
using namespace std;
namespace fs = std::filesystem;

// Функция для чтения вектора из файла
vector<int> read_from_file(const string& filename)
{
    vector<int> numbers;
    ifstream file(filename);

    if (file.is_open()) {
        char bit;
        while (file.get(bit)) {
            if (bit == '0' || bit == '1') {
                numbers.push_back(bit - '0');  
            }
        }
        file.close();
        
    }
    else {
        cout << "Ошибка при открытии файла: " << filename << endl;
    }

    return numbers;
}

void print_vec(vector<int>& numbers)
{
    for (int i = 0; i < numbers.size(); i++)
    {
        cout << numbers[i];
    }
}

int vector_summ(vector<int>& numbers)
{
    int summ = 0;
    for (int i = 0; i < numbers.size(); i++)
    {
        if (numbers[i] == 0)
            summ += -1;
        if (numbers[i] == 1)
            summ += 1;
    }
    return summ;
}

int summary(vector<int>& numbers)
{
    int summ = 0;
    for (int i = 0; i < numbers.size(); i++)
        summ += numbers[i];
    return summ;
}


int summary_V(vector<int>& numbers)
{
    int summ = 0;
    for (int i = 0; i < numbers.size() - 1; i++)
    {
        if (numbers[i] == numbers[i + 1])
            summ += 0;
        if (numbers[i] != numbers[i + 1])
            summ += 1;
    }
    return summ;
}


double test_1(vector<int>& numbers)
{
    int N = numbers.size();
    int summ = vector_summ(numbers);

    double formula_S_n = (1.0 / (sqrt(N))) * abs(summ);

    double Pvalue = erfc(formula_S_n / sqrt(2));

    return Pvalue;
}

double test_2(vector<int>& numbers)
{
    double P_value = 0;

    int N = numbers.size();
    int summ = summary(numbers);
    int V = summary_V(numbers);

    double psi = (1.0 / N) * summ;
    if (abs(psi - 0.5) >= (2.0 / sqrt(N)))
        P_value = 0;
    else
    {
        P_value = erfc(abs(V - 2 * N * psi * (1 - psi)) / (2 * sqrt(2 * N) * psi * (1 - psi)));
    }
    return P_value;
}


double test_3(vector<int>& numbers)
{
    int N = numbers.size();
    int M = 8;
    int blocks = N / M;

    int v1 = 0, v2 = 0, v3 = 0, v4 = 0;

    for (int b = 0; b < blocks; b++)
    {
        int max_run = 0;
        int current_run = 0;

        for (int i = 0; i < M; i++)
        {
            int bit = numbers[b * M + i];

            if (bit == 1)
            {
                current_run++;
                if (current_run > max_run)
                    max_run = current_run;
            }
            else
            {
                current_run = 0;
            }
        }

        if (max_run <= 1) v1++;
        else if (max_run == 2) v2++;
        else if (max_run == 3) v3++;
        else v4++;
    }

    double pi[4] = { 0.2148, 0.3672, 0.2305, 0.1875 };
    int v[4] = { v1, v2, v3, v4 };

    double chi2 = 0.0;

    for (int i = 0; i < 4; i++)
    {
        double expected = blocks * pi[i];
        chi2 += pow(v[i] - expected, 2) / expected;
    }

    double P_value = exp(-chi2 / 2.0) * (1 + chi2 / 2.0);

    return P_value;

}

void process_file(const string& filename, const string& file_label) {
    cout << "\n======================================" << endl;
    cout << "Обработка файла: " << file_label << endl;
    cout << "Читаем файл из: " << filename << endl;

    vector<int> numbers = read_from_file(filename);

    if (numbers.empty()) {
        cout << "Вектор пуст! Пропускаем файл." << endl;
        return;
    }

    cout << "Размер последовательности: " << numbers.size() << " бит" << endl;
    cout << "Первые 50 бит: ";
    for (int i = 0; i < min(50, (int)numbers.size()); i++) {
        cout << numbers[i];
    }
    cout << (numbers.size() > 50 ? "..." : "") << endl;

    double test1 = test_1(numbers);
    double test2 = test_2(numbers);
    double test3 = test_3(numbers);

    cout << "\nРезультаты тестов:" << endl;
    cout << "Test 1 (Частотный побитовый тест): P-value = " << test1 << endl;
    cout << "Test 2 (Тест на одинаковые подряд идущие биты): P-value = " << test2 << endl;
    cout << "Test 3 (Тест на максимальную длину серии в блоке): P-value = " << test3 << endl;

    
    cout << "\nИнтерпретация результатов (при уровне значимости 0.01):" << endl;
    cout << "Test 1: " << (test1 < 0.01 ? "НЕ РАНДОМНАЯ" : "рандомизированная") << endl;
    cout << "Test 2: " << (test2 < 0.01 ? "НЕ РАНДОМНАЯ" : "рандомизированная") << endl;
    cout << "Test 3: " << (test3 < 0.01 ? "НЕ РАНДОМНАЯ" : "рандомизированная") << endl;
}

int main() {
#if _MSC_VER
    system("chcp 65001 > nul");
#endif
    ios_base::sync_with_stdio(false);

    string source_dir = SOURCE_DIR;  // путь к текущей папке (task2)
    fs::path lab2_path = fs::path(source_dir).parent_path();  // 

    // Обрабатываем оба файла
    string filename_cpp = (lab2_path / "task2" / "sequence_c++.txt").string();
    string filename_java = (lab2_path / "task2" / "sequence_java.txt").string();

    process_file(filename_cpp, "sequence_c++.txt");
    process_file(filename_java, "sequence_java.txt");

    cout << "\n======================================" << endl;
    cout << "Обработка всех файлов завершена." << endl;

    return 0;
}
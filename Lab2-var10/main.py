from tests.nist_tests import read_sequence, run_all_tests
import sys

def main():
    seq_cpp = read_sequence("sequences/seq_cpp.txt")
    seq_java = read_sequence("sequences/seq_java.txt")

    with open("results.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        print("=" * 60)
        print("ЛАБОРАТОРНАЯ РАБОТА №2 – РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 60)
        run_all_tests(seq_cpp, "C++ (mt19937)")
        run_all_tests(seq_java, "Java (Random)")
        sys.stdout = sys.__stdout__

    with open("results.txt", "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()
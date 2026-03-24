from tests.nist_tests import read_sequence, run_all_tests

def main():
    seq_cpp = read_sequence("sequences/seq_cpp.txt")
    seq_java = read_sequence("sequences/seq_java.txt")

    print("=" * 50)
    print("Тестирование последовательности из C++ (mt19937)")
    run_all_tests(seq_cpp)

    print("\n" + "=" * 50)
    print("Тестирование последовательности из Java (Random)")
    run_all_tests(seq_java)

if __name__ == "__main__":
    main()

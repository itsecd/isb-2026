from config import SEQUENCE_FILES, OUTPUT_PATH, SIGNIFICANCE_LEVEL
from nist_tests import monobit_test, runs_test, longest_block_run


def load_sequence(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read().strip()


def run_all_tests(sequence: str) -> tuple[list[float], bool]:
    tests = [monobit_test, runs_test, longest_block_run]
    values = [test(sequence) for test in tests]
    success = all(value >= SIGNIFICANCE_LEVEL for value in values)
    return values, success


def format_result(name: str, values: list[float], passed: bool) -> str:
    status = "PASSED" if passed else "FAILED"
    return (
        f"{name.upper():7} | "
        f"{values[0]:.6f} | "
        f"{values[1]:.6f} | "
        f"{values[2]:.6f} | "
        f"{status}\n"
    )


def main() -> None:
    results = []

    for language, path in SEQUENCE_FILES.items():
        sequence = load_sequence(path)
        test_values, passed = run_all_tests(sequence)
        results.append(format_result(language, test_values, passed))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output:
        output.write("Lang   | Frequency | Runs | LongestRun | Result\n")
        for line in results:
            output.write(line)


if __name__ == "__main__":
    main()

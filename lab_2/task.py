from constants import BITS_C, BITS_CPP, BITS_JAVA

def frequency_bitwise_test() -> None:
    ...

def analyse(bits: str) -> None:
    ...

def main():
    with open(BITS_C, mode="r") as f:
        analyse(f.read())

    with open(BITS_CPP, mode="r") as f:
        analyse(f.read())

    with open(BITS_JAVA, mode="r") as f:
        analyse(f.read())

if __name__ == "__main__":
    main()
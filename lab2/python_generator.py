import argparse
import random


def generate_random_sequence () -> str:
    """
    генерирует псевдослучайную последовательность из 128 бит
    """
    sequence = ""

    for i in range(128):
        sequence_element = random.randint(0,1)
        sequence += str(sequence_element)
    
    return sequence


def write_file (sequence:str, output_file: str) -> None:
    """
    записывает последовательность в файл
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(sequence)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", '--output_file_name', type=str, default='python_sequence.txt', help='name of output file')
    args = parser.parse_args()

    print(f"The name of output file is: {args.output_file_name}")

    try:
        sequence = generate_random_sequence()
        write_file(sequence, args.output_file_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__" :
    main()
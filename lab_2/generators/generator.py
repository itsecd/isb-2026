import argparse
import random

def rand_bits(c: int) -> list:
    bits = []
    for _ in range(c):
            bits.append(random.randint(0, 1))
    return bits 


def file_writter(filename: str, bits: list) -> None:
    try:
        with open(filename, "w") as file:
            for i in bits:
                 file.write(str(i))
    except Exception as e:
        raise e
    

def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--count", "-c", default=128, type=int, help="число бит на выдачу.")
    parser.add_argument("--writefile", "-w", default="lab_2/gen_bits/python_gen.txt", type=str, help="Путь к файлу для записи результата.")
    args = parser.parse_args()

    try:
         file_writter(args.writefile, rand_bits(args.count))
    except Exception as e:
        print (f"{e}")

if __name__ == "__main__":
     main()
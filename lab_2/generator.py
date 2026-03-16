import random


def generate(length, filename):
    """Генерация последовательности и сохранение в файл"""

    result = ""
    for _ in range(length):
        result += str(random.randint(0, 1))
    
    with open(filename, 'w') as f:
        f.write(result)
    
    return result


def main() -> None:
    try:
        seq = generate(128, 'sequence_py.txt')
        print(seq)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
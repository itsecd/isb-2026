import random
from const import BIT, FILENAME


def generate_sequence(length: int) -> list[int]:
    """
    Генерирует случайную двоичную последовательность заданной длины
    Использует встроенный генератор random.getrandbits для эффективности
    """
    rand_bits = random.getrandbits(length)
    binary_str = format(rand_bits, '0{}b'.format(length))
    return [int(bit) for bit in binary_str]


def write_bits_to_file(filename: str, bits: list[int]) -> None:
    """Записывает последовательность битов в файл."""
    with open(filename, 'w') as f:
        for bit in bits:
            f.write(str(bit))


def print_bits(bits: list[int], group_size: int = 8) -> None:
    """Выводит биты на экран, группируя для удобства."""
    for i in range(0, len(bits), group_size):
        group = bits[i:i+group_size]
        print(''.join(map(str, group)), end=' ')
    print()


def main():
    bits = generate_sequence(BIT)
    write_bits_to_file(FILENAME, bits)


if __name__ == "__main__":
    main()

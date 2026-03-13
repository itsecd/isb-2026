import math
import os


def get_column_order(key):
    """
    Определяет порядок столбцов на основе ключа
    """
    sorted_pairs = sorted([(char, i) for i, char in enumerate(key)])

    order = [0] * len(key)
    for new_pos, (_, original_pos) in enumerate(sorted_pairs):
        order[original_pos] = new_pos

    return order


def encrypt(text, key):
    """
    Шифрование
    """

    text = text.replace('\n', ' ').upper()
    cols = len(key)
    rows = (len(text) + cols - 1) // cols

    text = text.ljust(rows * cols)

    table = [list(text[i*cols:(i+1)*cols]) for i in range(rows)]

    col_order = get_column_order(key)

    result = []
    for read_pos in range(cols):
        col = col_order.index(read_pos)
        for row in range(rows):
            result.append(table[row][col])

    return ''.join(result)


def decrypt(encrypted, key):
    """
    Дешифрование
    """
    cols = len(key)
    rows = (len(encrypted) + cols - 1) // cols

    col_order = get_column_order(key)

    table = [[''] * cols for _ in range(rows)]

    pos = 0
    for read_pos in range(cols):
        col = col_order.index(read_pos)
        for row in range(rows):
            if pos < len(encrypted):
                table[row][col] = encrypted[pos]
                pos += 1

    return ''.join(''.join(row) for row in table).rstrip()


def main():
    key = "ЛИЛИЯ"
    input_file = "input.txt"

    if not os.path.exists(input_file):
        print(f"Ошибка: файл {input_file} не найден")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    print("Задание 1.")
    print(f"Ключ: {key}")
    print(f"Длина ключа: {len(key)}")
    print(f"Исходный текст: {len(text)} символов")

    encrypted = encrypt(text, key)

    with open("encrypted.txt", "w", encoding='utf-8') as f:
        f.write(encrypted)

    print(f"\n Шифрование. Первые 100 символов:\n{encrypted[:100]}...")

    decrypted = decrypt(encrypted, key)

    with open("decrypted_check.txt", "w", encoding='utf-8') as f:
        f.write(decrypted)

    print(f"\n Дешифровка. Первые 100 символов:\n{decrypted[:100]}...")

    original_clean = text.replace('\n', ' ').upper().rstrip()
    decrypted_clean = decrypted.rstrip()

    if original_clean == decrypted_clean:
        print("\nУспешная расшифровка. Текст совпал с оригиналом.")
    else:
        print("\nТекст не совпал с оригиналом")

if __name__ == "__main__":
    main()

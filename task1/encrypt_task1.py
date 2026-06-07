"""
Модуль шифрования методом блочной двойной перестановки.
Содержит функции для загрузки/сохранения текста, предобработки,
генерации ключей и выполнения перестановок по строкам и столбцам.
"""

import random
from constants import RUS_ALPHABET

def load_text(filename):
    """
    Загружает текст из файла в кодировке UTF-8.

    Args:
        filename (str): Имя файла для чтения.

    Returns:
        str: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не существует.
        OSError: При других ошибках ввода-вывода.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден.")
    except OSError as e:
        raise OSError(f"Ошибка при чтении файла {filename}: {e}")

def save_text(filename, text):
    """
    Сохраняет текст в файл в кодировке UTF-8.

    Args:
        filename (str): Имя файла для записи.
        text (str): Текст для сохранения.

    Raises:
        OSError: При ошибках ввода-вывода.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"[OK] {filename}")
    except OSError as e:
        raise OSError(f"Ошибка при записи файла {filename}: {e}")

def preprocess(text):
    """
    Приводит текст к нижнему регистру и удаляет все символы,
    кроме букв русского алфавита и пробела.

    Args:
        text (str): Исходный текст.

    Returns:
        str: Очищенный текст.
    """
    allowed = set(RUS_ALPHABET + ' ')
    text = text.lower()
    return ''.join(ch for ch in text if ch in allowed)

def repeat_key(key, length):
    """
    Повторяет ключ до заданной длины.

    Args:
        key (str): Исходный ключ.
        length (int): Необходимая длина.

    Returns:
        str: Ключ, повторённый или обрезанный до длины `length`.
    """
    key = key.lower()
    if not key:
        key = 'а'
    return (key * (length // len(key) + 1))[:length]

def get_permutation_order(key):
    """
    Определяет порядок перестановки столбцов/строк на основе ключа.
    Индексы сортируются по лексикографическому порядку символов ключа.

    Args:
        key (str): Ключ (строка) для определения перестановки.

    Returns:
        list[int]: Список индексов в порядке, соответствующем сортировке ключа.
    """
    indices = list(range(len(key)))
    indices.sort(key=lambda i: key[i])
    return indices

def apply_permutation(matrix, order, axis='cols'):
    """
    Применяет перестановку к матрице по строкам или столбцам.

    Args:
        matrix (list[list]): Двумерный список (матрица) символов.
        order (list[int]): Новый порядок индексов.
        axis (str): Ось перестановки: 'cols' (столбцы) или 'rows' (строки).

    Returns:
        list[list]: Матрица после перестановки.
    """
    R = len(matrix)
    C = len(matrix[0]) if R > 0 else 0
    if axis == 'cols':
        return [[matrix[r][order[c]] for c in range(C)] for r in range(R)]
    else:  # rows
        return [matrix[order[r]] for r in range(R)]

def encrypt_block(block, rows, cols, key_cols, key_rows):
    """
    Шифрует один блок текста двойной перестановкой:
    сначала переставляются столбцы, затем строки.

    Args:
        block (str): Исходный блок длиной rows * cols.
        rows (int): Количество строк в матрице.
        cols (int): Количество столбцов в матрице.
        key_cols (str): Ключ для перестановки столбцов.
        key_rows (str): Ключ для перестановки строк.

    Returns:
        str: Зашифрованный блок той же длины.
    """
    matrix = []
    for i in range(rows):
        start = i * cols
        matrix.append(list(block[start:start+cols]))

    col_key = repeat_key(key_cols, cols)
    col_order = get_permutation_order(col_key)
    matrix = apply_permutation(matrix, col_order, 'cols')

    row_key = repeat_key(key_rows, rows)
    row_order = get_permutation_order(row_key)
    matrix = apply_permutation(matrix, row_order, 'rows')

    return ''.join(''.join(row) for row in matrix)

def encrypt_text(plaintext, rows, cols, key_cols, key_rows):
    """
    Разбивает текст на блоки размера rows*cols и шифрует каждый блок.
    Последний блок при необходимости дополняется случайными буквами из алфавита.

    Args:
        plaintext (str): Исходный открытый текст.
        rows (int): Количество строк в матрице.
        cols (int): Количество столбцов в матрице.
        key_cols (str): Ключ для перестановки столбцов.
        key_rows (str): Ключ для перестановки строк.

    Returns:
        str: Полный зашифрованный текст.

    Raises:
        ValueError: Если rows * cols == 0.
    """
    block_size = rows * cols
    if block_size == 0:
        raise ValueError("Размер блока (rows * cols) не может быть нулевым.")
    blocks = []
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        if len(block) < block_size:
            filler = ''.join(random.choice(RUS_ALPHABET) for _ in range(block_size - len(block)))
            block += filler
        blocks.append(block)

    encrypted_blocks = [encrypt_block(b, rows, cols, key_cols, key_rows) for b in blocks]
    return ''.join(encrypted_blocks)

def main():
    """
    Основная функция: загружает текст из task1_original.txt,
    очищает его, запрашивает параметры шифрования у пользователя,
    выполняет шифрование и сохраняет результат в task1_encrypted.txt,
    а параметры ключей — в task1_key.txt.

    Raises:
        FileNotFoundError: Если исходный файл не найден.
        ValueError: При некорректном вводе числа строк/столбцов.
        OSError: При ошибках записи выходных файлов.
    """
    print("=== Задание 1: блочная двойная перестановка ===")
    try:
        original = load_text("task1_original.txt")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return
    except OSError as e:
        print(f"Ошибка ввода-вывода: {e}")
        return

    processed = preprocess(original)
    print(f"Длина текста после очистки: {len(processed)}")

    try:
        rows = int(input("Введите количество строк R: "))
        cols = int(input("Введите количество столбцов C: "))
    except ValueError:
        print("Ошибка: необходимо ввести целое число.")
        return

    key_cols = input("Ключ для столбцов: ").strip() or "столбец"
    key_rows = input("Ключ для строк: ").strip() or "строка"

    try:
        ciphertext = encrypt_text(processed, rows, cols, key_cols, key_rows)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    try:
        save_text("task1_encrypted.txt", ciphertext)
        with open("task1_key.txt", "w", encoding='utf-8') as f:
            f.write(f"ROWS={rows}\nCOLS={cols}\nKEY_COLS={key_cols}\nKEY_ROWS={key_rows}\n")
        print("[OK] task1_key.txt")
        print("Готово.")
    except OSError as e:
        print(f"Ошибка при сохранении результатов: {e}")

if __name__ == "__main__":
    random.seed()
    main()
import math


def get_column_order_from_key(keyword):
    """
    Преобразует ключевое слово в порядок столбцов
    """
    letters = list(keyword.upper())
    indexed_letters = [(letters[i], i) for i in range(len(letters))]
    sorted_letters = sorted(indexed_letters, key=lambda x: x[0])

    column_order = [0] * len(letters)
    for new_pos, (_, old_pos) in enumerate(sorted_letters):
        column_order[old_pos] = new_pos

    return column_order


def encrypt(text, keyword):
    """Шифрование методом постолбцовой транспозиции"""
    key = get_column_order_from_key(keyword)
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)

    print(f"\nКлючевое слово: '{keyword}'")
    print(f"Порядок столбцов: {key}")

    table = []
    idx = 0
    for row in range(num_rows):
        current_row = []
        for col in range(num_cols):
            if idx < len(text):
                current_row.append(text[idx])
            else:
                current_row.append(' ')
            idx += 1
        table.append(current_row)

    result = []
    for col in sorted(range(num_cols), key=lambda x: key[x]):
        for row in range(num_rows):
            result.append(table[row][col])

    return ''.join(result)


def decrypt(encrypted_text, keyword):
    """Дешифрование методом постолбцовой транспозиции"""
    key = get_column_order_from_key(keyword)
    num_cols = len(key)
    num_rows = math.ceil(len(encrypted_text) / num_cols)

    table = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]

    total_cells = num_rows * num_cols
    empty_cells = total_cells - len(encrypted_text)

    col_heights = {}
    for col in range(num_cols):
        if col >= num_cols - empty_cells:
            col_heights[col] = num_rows - 1
        else:
            col_heights[col] = num_rows

    idx = 0
    read_order = sorted(range(num_cols), key=lambda x: key[x])

    for col in read_order:
        for row in range(col_heights[col]):
            if idx < len(encrypted_text):
                table[row][col] = encrypted_text[idx]
                idx += 1

    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            result.append(table[row][col])

    return ''.join(result).rstrip()
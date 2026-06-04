import random

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def save_text(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[OK] {filename}")

def preprocess(text):
    allowed = set('абвгдежзийклмнопрстуфхцчшщъыьэюя ')
    text = text.lower()
    return ''.join(ch for ch in text if ch in allowed)

def repeat_key(key, length):
    key = key.lower()
    if not key:
        key = 'а'
    return (key * (length // len(key) + 1))[:length]

def get_permutation_order(key):
    indices = list(range(len(key)))
    indices.sort(key=lambda i: key[i])
    return indices

def apply_permutation(matrix, order, axis='cols'):
    R = len(matrix)
    C = len(matrix[0]) if R > 0 else 0
    if axis == 'cols':
        return [[matrix[r][order[c]] for c in range(C)] for r in range(R)]
    else:
        return [matrix[order[r]] for r in range(R)]

def encrypt_block(block, rows, cols, key_cols, key_rows):
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
    block_size = rows * cols
    blocks = []
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        if len(block) < block_size:
            alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
            filler = ''.join(random.choice(alphabet) for _ in range(block_size - len(block)))
            block += filler
        blocks.append(block)
    encrypted_blocks = [encrypt_block(b, rows, cols, key_cols, key_rows) for b in blocks]
    return ''.join(encrypted_blocks)

def main():
    print("=== Задание 1: блочная двойная перестановка ===")
    original = load_text("task1_original.txt")
    processed = preprocess(original)
    print(f"Длина текста после очистки: {len(processed)}")

    rows = int(input("Введите количество строк R: "))
    cols = int(input("Введите количество столбцов C: "))
    key_cols = input("Ключ для столбцов: ").strip() or "столбец"
    key_rows = input("Ключ для строк: ").strip() or "строка"

    ciphertext = encrypt_text(processed, rows, cols, key_cols, key_rows)
    save_text("task1_encrypted.txt", ciphertext)

    with open("task1_key.txt", "w", encoding='utf-8') as f:
        f.write(f"ROWS={rows}\nCOLS={cols}\nKEY_COLS={key_cols}\nKEY_ROWS={key_rows}\n")
    print("[OK] task1_key.txt")
    print("Готово.")

if __name__ == "__main__":
    random.seed()
    main()
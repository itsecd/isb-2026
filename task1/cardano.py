import random
import math

def read_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', ' ')

def write_text(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def write_key(filename, grid, size):
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(size):
            row = ''.join(['1' if grid[i][j] else '0' for j in range(size)])
            f.write(row + '\n')

def create_cardano_grid(size):
    # Создаём пустую решётку
    grid = [[False] * size for _ in range(size)]
    
    # Количество отверстий: ровно четверть от всех ячеек
    total_cells = size * size
    holes_needed = total_cells // 4
    
    # Выбираем случайные позиции для отверстий
    positions = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(positions)
    
    for k in range(holes_needed):
        i, j = positions[k]
        grid[i][j] = True
    
    return grid

def rotate_grid_90(grid):
    size = len(grid)
    rotated = [[False] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            rotated[j][size - 1 - i] = grid[i][j]
    return rotated

def encrypt_cardano(text, grid):
    size = len(grid)
    # Создаём пустую сетку для шифротекста
    encrypted_grid = [[' '] * size for _ in range(size)]
    
    text_index = 0
    current_grid = grid
    
    for rotation in range(4):
        for i in range(size):
            for j in range(size):
                if current_grid[i][j] and text_index < len(text):
                    encrypted_grid[i][j] = text[text_index]
                    text_index += 1
        # Поворачиваем решётку для следующего прохода
        current_grid = rotate_grid_90(current_grid)
    
    # Если текст не влез, дополним пробелами
    while text_index < len(text):
        # Ищем первую пустую ячейку
        for i in range(size):
            for j in range(size):
                if encrypted_grid[i][j] == ' ' and text_index < len(text):
                    encrypted_grid[i][j] = text[text_index]
                    text_index += 1
    
    # Преобразуем сетку в строку (построчно)
    encrypted_text = ''
    for row in encrypted_grid:
        encrypted_text += ''.join(row) + '\n'
    
    return encrypted_text.strip()

def main():
    original_text = read_text('original_text.txt').upper()

    text_len = len(original_text)
    size = math.ceil(math.sqrt(text_len))
    if size % 2 != 0:
        size += 1

    grid = create_cardano_grid(size)

    encrypted_text = encrypt_cardano(original_text, grid)

    write_text('encrypted_text.txt', encrypted_text)
    write_key('key_cardano.txt', grid, size)

    print(f"Размер решётки: {size}x{size}")
    print(f"Длина текста: {text_len} символов")
    print(f"Файлы сохранены: encrypted_text.txt, key_cardano.txt")

if __name__ == "__main__":
    main()
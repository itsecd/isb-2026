import random
import math

def read_text(filename):
    """Чтение текста из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', ' ')

def write_text(filename, text):
    """Запись текста в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def write_key(filename, grid, size):
    """Запись ключа (решётки) в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(size):
            row = ''.join(['1' if grid[i][j] else '0' for j in range(size)])
            f.write(row + '\n')

def read_key(filename, size):
    """Чтение ключа (решётки) из файла"""
    grid = [[False] * size for _ in range(size)]
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= size:
                break
            for j, ch in enumerate(line.strip()):
                if j >= size:
                    break
                grid[i][j] = (ch == '1')
    return grid

def create_cardano_grid(size):
    """Создание случайной решётки Кардано"""
    grid = [[False] * size for _ in range(size)]
    total_cells = size * size
    holes_needed = total_cells // 4
    
    positions = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(positions)
    
    for k in range(holes_needed):
        i, j = positions[k]
        grid[i][j] = True
    
    return grid

def rotate_grid_90(grid):
    """Поворот решётки на 90 градусов по часовой стрелке"""
    size = len(grid)
    rotated = [[False] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            rotated[j][size - 1 - i] = grid[i][j]
    return rotated

def encrypt_cardano(text, grid):
    """Шифрование текста методом решётки Кардано"""
    size = len(grid)
    encrypted_grid = [[' '] * size for _ in range(size)]
    
    text_index = 0
    current_grid = grid
    
    # 4 поворота решётки
    for rotation in range(4):
        for i in range(size):
            for j in range(size):
                if current_grid[i][j] and text_index < len(text):
                    encrypted_grid[i][j] = text[text_index]
                    text_index += 1
        current_grid = rotate_grid_90(current_grid)
    
    # Если текст не влез, заполняем оставшиеся ячейки
    while text_index < len(text):
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

def decrypt_cardano(encrypted_text, grid):
    """Дешифрование текста, зашифрованного методом решётки Кардано"""
    # Преобразуем зашифрованный текст обратно в сетку
    lines = encrypted_text.strip().split('\n')
    size = len(grid)
    
    # Если размер сетки не совпадает с количеством строк
    if len(lines) != size:
        raise ValueError(f"Размер сетки ({size}) не совпадает с количеством строк в файле ({len(lines)})")
    
    # Создаём сетку из зашифрованного текста
    encrypted_grid = []
    for line in lines:
        # Если строка короче size, дополняем пробелами
        row = list(line.ljust(size))
        encrypted_grid.append(row)
    
    # Восстанавливаем текст
    decrypted_chars = []
    current_grid = grid
    
    # Читаем в том же порядке поворотов, что и при шифровании
    for rotation in range(4):
        for i in range(size):
            for j in range(size):
                if current_grid[i][j]:
                    # Добавляем символ из соответствующей ячейки
                    decrypted_chars.append(encrypted_grid[i][j])
        current_grid = rotate_grid_90(current_grid)
    
    # Объединяем все символы в строку
    decrypted_text = ''.join(decrypted_chars)
    
    # Удаляем возможные пробелы в конце (если текст был короче)
    return decrypted_text.rstrip()
    
def main():
    try:
        original_text = read_text('original_text.txt').upper()
        text_len = len(original_text)
        
        # Определяем размер решётки
        size = math.ceil(math.sqrt(text_len))
        if size % 2 != 0:
            size += 1

        print(f"Длина: {text_len} символов")
        print(f"\nРазмер решётки: {size}x{size}")
        
        # Создаём решётку и шифруем
        grid = create_cardano_grid(size)
        encrypted_text = encrypt_cardano(original_text, grid)
        
        # Сохраняем результаты
        write_text('encrypted_text.txt', encrypted_text)
        write_key('key_cardano.txt', grid, size)
        
        print(f"\nШифрование завершено")
        
    except FileNotFoundError:
        print("\nФайл 'original_text.txt' не найден")
       

if __name__ == "__main__":
    main()
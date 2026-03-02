import os

SIZE = 6  # так как 36 ячеек

def read_key_txt(filename):
    """Читает квадрат Полибия из текстового файла и создает маппинг для JSON."""
    if not os.path.exists(filename):
        print(f"Ошибка: файл {filename} не найден!")
        return None, None
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    square = []
    for line in lines[1:]:
        line = line.rstrip('\n')
        if line:
            chars = line[4:].split('   ')
            square.append(chars)
    
    if len(square) != SIZE:
        print(f"Ошибка: в файле {len(square)} строк, ожидалось {SIZE}")
        return None, None
    
    encrypt_map = {}
    alphabet = ""
    
    for i in range(SIZE):
        if len(square[i]) != SIZE:
            print(f"Ошибка: в строке {i+1} {len(square[i])} элементов, ожидалось {SIZE}")
            return None, None
        
        for j in range(SIZE):
            char = square[i][j]
            if char != '*':
                if char == '_':
                    encrypt_map[' '] = f"{i+1:01d}{j+1:01d}"
                    alphabet += ' '
                else:
                    encrypt_map[char] = f"{i+1:01d}{j+1:01d}"
                    alphabet += char
    
    return encrypt_map, alphabet

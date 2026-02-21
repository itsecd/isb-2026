def load_key_from_table(filename):
    """Читает таблицу Полибия из файла и возвращает словарь буква → код"""
    key = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) < 7:
            continue
        row = parts[0] 
        letters = parts[1:7]
        for col, letter in enumerate(letters, start=1):
            if letter == 'пробел':
                letter = ' '
            if letter != '-': 
                code = row + str(col)
                key[letter] = code
    return key

key = load_key_from_table('key.txt')

with open('input_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

encrypted = []
for ch in text:
    if ch in key:
        encrypted.append(key[ch])
    else:
        continue

with open('encrypted.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(encrypted))

print("Зашифрованный текст сохранён в encrypted.txt") 
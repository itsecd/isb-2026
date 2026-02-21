key = {}
with open('key.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(' - ')
        if len(parts) == 2:
            symbol, letter = parts
            if letter == 'пробел':
                letter = ' '
            key[symbol] = letter

with open('cod9.txt', 'r', encoding='utf-8') as f:
    encrypted = f.read()

decrypted = []
for ch in encrypted:
    if ch == '\n':
        decrypted.append('\n') 
    else:
        decrypted.append(key.get(ch, ch))

with open('decrypted.txt', 'w', encoding='utf-8') as f:
    f.write(''.join(decrypted))

print("Расшифрованный текст сохранён в decrypted.txt")
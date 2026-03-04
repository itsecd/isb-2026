with open('cod18.txt', 'r', encoding='utf-8') as f:
    cipher = f.read().upper()

freq = {}
for c in cipher:
    freq[c] = freq.get(c, 0) + 1

sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

print('Частоты символов:')
print('Символ | Количество')
print('-------|-----------')
for c, n in sorted_freq[:15]:
    print(f'   {c}   |    {n}')


replaces = {}
current = cipher

while True:
    print('\nПолный текст сейчас:\n')
    print(current) 
    
    print('\nТекущие замены:')
    if replaces:
        for old, new in replaces.items():
            if new == ' ':
                print(f'  {old} -> ПРОБЕЛ')
            else:
                print(f'  {old} -> {new}')
    else:
        print('  Замен нет')
    
    old = input('\nКакой символ заменить? (Enter - выход) ').strip().upper()
    if not old:
        break
    
    new = input(f'На что заменить "{old}"? : ').strip()
    
    if new.lower() == 'пробел':
        replaces[old] = ' '
        print(f'{old} -> ПРОБЕЛ')
    else:
        replaces[old] = new.upper()
        print(f'{old} -> {new.upper()}')
    
    current = ''
    for c in cipher:
        if c in replaces:
            current += replaces[c]
        else:
            current += c

with open('decrypted.txt', 'w', encoding='utf-8') as f:
    f.write(current)

with open('found_key.txt', 'w', encoding='utf-8') as f:
    f.write('Ключ:\n')
    for old, new in replaces.items():
        if new == ' ':
            f.write(f'{old} -> ПРОБЕЛ\n')
        else:
            f.write(f'{old} -> {new}\n')

print('- decrypted.txt (расшифрованный текст)')
print('- found_key.txt (найденный ключ)')
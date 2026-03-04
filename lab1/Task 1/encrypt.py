ALPH = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

DEFAULT_KEY = 'ЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЕДГВБА '

with open('original.txt', 'r', encoding='utf-8') as f:
    text = f.read().upper()

print('Алфавит:', ALPH)
print('\nКлюч по умолчанию:', DEFAULT_KEY)
print('(Нажмите Enter, чтобы использовать его, или введите свой ключ)')

user_key = input('Ваш ключ: ').upper()
if user_key == '':
    KEY = DEFAULT_KEY
else:
    KEY = user_key

if len(KEY) != len(ALPH):
    print(f'Ошибка! Длина ключа должна быть {len(ALPH)} символа')
    print('Будет использоваться ключ по умолчанию')
    KEY = DEFAULT_KEY

print('\nИспользуемый ключ:', KEY)

cipher_dict = {}
for i in range(len(ALPH)):
    cipher_dict[ALPH[i]] = KEY[i]

encrypted = ''
for char in text:
    if char in cipher_dict:
        encrypted += cipher_dict[char]
    else:
        encrypted += char

with open('encrypted.txt', 'w', encoding='utf-8') as f:
    f.write(encrypted)

decipher_dict = {}
for i in range(len(ALPH)):
    decipher_dict[KEY[i]] = ALPH[i]

decrypted = ''
for char in encrypted:
    if char in decipher_dict:
        decrypted += decipher_dict[char]
    else:
        decrypted += char

with open('key.txt', 'w', encoding='utf-8') as f:
    f.write(f'Алфавит: {ALPH}\n')
    f.write(f'Ключ:    {KEY}\n')
    f.write(f'\nПроверка: расшифрованный текст совпадает с исходным? {decrypted == text}')

print('\n')
print('Проверка:')
print('Первые 100 символов исходного текста:')
print(text[:100])
print('\nПервые 100 символов после расшифровки:')
print(decrypted[:100])

if decrypted == text:
    print('\nРасшифрованный текст полностью совпадает с исходным')
else:
    print('\nРасшифрованный текст не совпадает с исходным')

print('Зашифрованный текст: encrypted.txt')
print('Ключ шифрования: key.txt')
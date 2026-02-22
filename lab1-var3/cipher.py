ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

def caesar_encrypt(text, shift):
    result = []
    for char in text:
        upper_char = char.upper()
        if upper_char in ALPHABET:
            idx = ALPHABET.index(upper_char)
            new_idx = (idx + shift) % len(ALPHABET)
            result.append(ALPHABET[new_idx])
        else:
            result.append(char)
    return ''.join(result)

try:
    SHIFT = int(input("Введите сдвиг для шифра Цезаря: "))
except ValueError:
    print("Ошибка: сдвиг должен быть числом!")
    exit(1)

try:
    with open('input_text.txt', 'r', encoding='utf-8') as f:
        original_text = f.read()
except FileNotFoundError:
    print('=' * len('Ошибка: файл input_text.txt не найден!'))
    print("\nОшибка: файл input_text.txt не найден!")
    print("Создайте файл input_text.txt с исходным текстом (не менее 500 символов)\n")
    exit(1)

text_length = len(original_text)

print('=' * len('Текст загружен, длина:      символов'))
print(f"Текст загружен, длина: {text_length} символов")
print('=' * len('Текст загружен, длина:      символов'))

encrypted_text = caesar_encrypt(original_text, SHIFT)

with open('encrypted.txt', 'w', encoding='utf-8') as f:
    f.write(encrypted_text)

with open('key.txt', 'w', encoding='utf-8') as f:
    f.write(f'Шифр: Цезарь\n')
    f.write(f'Алфавит: {ALPHABET}\n')
    f.write(f'Сдвиг: {SHIFT}\n')
    f.write('Таблица замены (исходный символ -> зашифрованный):\n')
    f.write('=' * 50 + '\n')
    for i, char in enumerate(ALPHABET):
        new_char = ALPHABET[(i + SHIFT) % len(ALPHABET)]
        if char == ' ':
            f.write(f'ПРОБЕЛ -> {new_char}\n')
        else:
            f.write(f'{char} -> {new_char}\n')

print(f"\nЗашифрованный текст:\n")
print(f"{encrypted_text}")

print("\n")
print('=' * len('Готово!'))
print(f"Готово!")
print('=' * len('Готово!'))
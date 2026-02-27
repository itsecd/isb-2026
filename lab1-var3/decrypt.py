from collections import Counter

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
REF_FREQ = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М',
            'Л', 'Д', 'К', 'П', 'У', 'Я', 'Ы', 'З', 'Ь', 'Б', 'Г',
            'Й', 'Ч', 'Ю', 'Х', 'Ж', 'Ц', 'Ш', 'Щ', 'Э', 'Ф', 'Ъ']
LINE_WIDTH = 60

def load_cipher_text():
    # Загрузка зашифрованного текста из файла
    try:
        with open('cod3.txt', 'r', encoding='utf-8') as f:
            return f.read().lower()
    except FileNotFoundError:
        print("Ошибка: файл cod3.txt не найден!")
        return None
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def get_decrypted_text(cipher, mapping):
    # Получение расшифрованного текста
    result = ''
    for ch in cipher:
        if ch in mapping:
            result += mapping[ch].upper()
        else:
            result += ch
    return result

def save_results(cipher, mapping):
    # Сохранение результатов
    try:
        result = get_decrypted_text(cipher, mapping)

        with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
            f.write(result)

        with open('found_key.txt', 'w', encoding='utf-8') as f:
            f.write('КЛЮЧ ШИФРОВАНИЯ\n')
            f.write('=' * 15 + '\n')
            for letter in ALPHABET:
                found = False
                for cipher_char, plain_char in mapping.items():
                    if plain_char == letter:
                        if letter == ' ':
                            f.write(f'ПРОБЕЛ -> {cipher_char}\n')
                        else:
                            f.write(f'{letter} -> {cipher_char}\n')
                        found = True
                        break
                if not found:
                    if letter == ' ':
                        f.write('ПРОБЕЛ -> ?\n')
                    else:
                        f.write(f'{letter} -> ?\n')
        print('Сохранено')
    except IOError as e:
        print(f"Ошибка при сохранении: {e}")

def main():
    # Основная функция программы
    # Загрузка текста
    cipher = load_cipher_text()
    if cipher is None:
        return

    # Частотный анализ
    try:
        freq = Counter(cipher)
        print('ЧАСТОТНЫЙ АНАЛИЗ:')
        print('=' * len('ЧАСТОТНЫЙ АНАЛИЗ:'))

        for i, (char, count) in enumerate(freq.most_common()):
            print(f"{i+1:2d}. '{char}' = {count:4d} раз(а)")
    except Exception as e:
        print(f"Ошибка при частотном анализе: {e}")
        return

    mapping = {}

    print('=' * len('  show             - показать результат'))
    print('\nКОМАНДЫ:')
    print('  <символ> <буква> - добавить замену')
    print('  show             - показать результат')
    print('  save             - сохранить')
    print('  exit             - выход')
    print('=' * len('  show             - показать результат'))

    # Основной цикл
    while True:
        try:
            cmd = input('\n> ').strip()

            if cmd == 'show':
                result = get_decrypted_text(cipher, mapping)
                print('\n' + '=' * LINE_WIDTH)
                print(result)
                print('=' * LINE_WIDTH)
                print(f'Замен: {len(mapping)}')

            elif cmd == 'save':
                save_results(cipher, mapping)

            elif cmd == 'exit':
                break

            else:
                parts = cmd.split()
                if len(parts) == 2:
                    c = parts[0].lower()
                    p = parts[1]

                    if p == 'пробел':
                        p = ' '
                    else:
                        p = p.upper()

                    if p not in ALPHABET and p != ' ':
                        print('Ошибка: такой буквы нет')
                        continue

                    mapping[c] = p
                    print(f'замена: {c} -> {p}')
        except KeyboardInterrupt:
            print("\nВыход по запросу пользователя")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
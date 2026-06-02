from collections import Counter

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
REF_FREQ = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М',
            'Л', 'Д', 'К', 'П', 'У', 'Я', 'Ы', 'З', 'Ь', 'Б', 'Г',
            'Й', 'Ч', 'Ю', 'Х', 'Ж', 'Ц', 'Ш', 'Щ', 'Э', 'Ф', 'Ъ']

LINE_WIDTH = 60


def read_cipher_file():
    try:
        with open('cod23.txt', 'r', encoding='utf-8') as file:
            return file.read().lower()
    except FileNotFoundError:
        print("Не удалось найти файл cod23.txt")
        return None
    except IOError as error:
        print(f"Ошибка чтения файла: {error}")
        return None


def analyze_frequencies(text):
    try:
        statistics = Counter(text)

        print('РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА')
        print('=' * len('РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА'))

        total = len(text)

        for index, (symbol, amount) in enumerate(statistics.most_common(), start=1):
            print(f"{index:2d}. '{symbol}' = {amount / total:.4f}")

        return statistics

    except Exception as error:
        print(f"Ошибка анализа: {error}")
        return None


def export_frequencies(statistics, total_chars, filename='frequencies.txt'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('СТАТИСТИКА ЧАСТОТ\n')
            file.write('=' * 40 + '\n')
            file.write('Символ | Частота\n')
            file.write('-' * 40 + '\n')

            for symbol, amount in statistics.most_common():
                if symbol == ' ':
                    symbol_name = 'ПРОБЕЛ'
                elif symbol == '\n':
                    symbol_name = 'НОВАЯ СТРОКА'
                else:
                    symbol_name = symbol

                file.write(
                    f"{symbol_name:12} | {amount / total_chars:.6f}\n"
                )

            file.write('=' * 40 + '\n')
            file.write(f'Количество символов: {total_chars}\n')

        print(f'Данные сохранены в {filename}')

    except IOError as error:
        print(f'Ошибка записи файла: {error}')


def decrypt_fragment(cipher_text, replacements):
    decoded = ''

    for symbol in cipher_text:
        if symbol in replacements:
            decoded += replacements[symbol].upper()
        else:
            decoded += symbol

    return decoded


def write_output(cipher_text, replacements):
    try:
        decoded_text = decrypt_fragment(cipher_text, replacements)

        with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
            file.write(decoded_text)

        with open('found_key.txt', 'w', encoding='utf-8') as file:
            file.write('НАЙДЕННЫЕ СООТВЕТСТВИЯ\n')
            file.write('=' * 25 + '\n')

            for letter in ALPHABET:
                exists = False

                for encrypted_char, original_char in replacements.items():
                    if original_char == letter:
                        if letter == ' ':
                            file.write(f'ПРОБЕЛ -> {encrypted_char}\n')
                        else:
                            file.write(f'{letter} -> {encrypted_char}\n')

                        exists = True
                        break

                if not exists:
                    if letter == ' ':
                        file.write('ПРОБЕЛ -> ?\n')
                    else:
                        file.write(f'{letter} -> ?\n')

        print('Результаты успешно сохранены')

    except IOError as error:
        print(f'Ошибка сохранения: {error}')


def start_program():
    cipher_text = read_cipher_file()

    if cipher_text is None:
        return

    total_chars = len(cipher_text)

    statistics = analyze_frequencies(cipher_text)

    if statistics is not None:
        export_frequencies(statistics, total_chars)

    replacements = {}

    print('\nДОСТУПНЫЕ КОМАНДЫ')
    print('=' * 30)
    print('  <символ> <буква>  - добавить соответствие')
    print('  show              - вывести текущий текст')
    print('  save              - сохранить результат')
    print('  exit              - завершить работу')
    print('=' * 30)

    while True:
        try:
            command = input('\n> ').strip()

            if command == 'show':
                decoded_text = decrypt_fragment(cipher_text, replacements)

                print('\n' + '=' * LINE_WIDTH)
                print(decoded_text)
                print('=' * LINE_WIDTH)
                print(f'Выполнено замен: {len(replacements)}')

            elif command == 'save':
                write_output(cipher_text, replacements)

            elif command == 'exit':
                break

            else:
                parts = command.split()

                if len(parts) == 2:
                    cipher_char = parts[0].lower()
                    plain_char = parts[1]

                    if plain_char == 'пробел':
                        plain_char = ' '
                    else:
                        plain_char = plain_char.upper()

                    if plain_char not in ALPHABET and plain_char != ' ':
                        print('Ошибка: символ отсутствует в алфавите')
                        continue

                    replacements[cipher_char] = plain_char
                    print(f'Добавлено: {cipher_char} -> {plain_char}')

        except KeyboardInterrupt:
            print('\nРабота программы прервана пользователем')
            break

        except Exception as error:
            print(f'Ошибка: {error}')


if __name__ == "__main__":
    start_program()
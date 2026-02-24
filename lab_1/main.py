from collections import Counter
import re
from datetime import datetime

# ===================== ЗАДАНИЕ 1: Квадрат Полибия =====================


class PolybiusSquare:
    """Класс для шифрования и дешифрования квадратом Полибия"""

    def __init__(self, alphabet=None, size=6):
        """
        Инициализация квадрата Полибия
        По умолчанию используем русский алфавит с цифрами в квадрате 6x6
        """
        if alphabet is None:
            self.alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя 0123456789.,!?-:;"
        else:
            self.alphabet = alphabet

        self.size = size
        self.square = self._create_square()

    def _create_square(self):
        """Создание квадрата Полибия из алфавита"""
        square = []
        alphabet_list = list(self.alphabet)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                index = i * self.size + j
                if index < len(alphabet_list):
                    row.append(alphabet_list[index])
                else:
                    row.append("")
            square.append(row)

        return square

    def print_square(self):
        """Вывод квадрата Полибия в консоль"""
        print("\nКвадрат Полибия:")
        print("   " + " ".join([f"{j + 1:2}" for j in range(self.size)]))
        for i in range(self.size):
            row_display = [f"{i + 1:2}"]  # Номер строки
            for j in range(self.size):
                cell = self.square[i][j] if self.square[i][j] else " "
                row_display.append(f"{cell:2}")
            print(" ".join(row_display))

    def get_encrypt_key(self):
        """Получение ключа для шифрования (буква -> код)"""
        key = {}
        for i in range(self.size):
            for j in range(self.size):
                char = self.square[i][j]
                if char:
                    key[char] = f"{i + 1}{j + 1}"
        return key

    def get_decrypt_key(self):
        """Получение ключа для дешифрования (код -> буква)"""
        key = {}
        for i in range(self.size):
            for j in range(self.size):
                char = self.square[i][j]
                if char:
                    key[f"{i + 1}{j + 1}"] = char
        return key

    def encrypt(self, text):
        """Шифрование текста квадратом Полибия"""
        # Приводим к нижнему регистру для единообразия
        text = text.lower()
        encrypted = []
        key = self.get_encrypt_key()

        for char in text:
            if char in key:
                encrypted.append(key[char])
            else:
                encrypted.append(char)

        # Объединяем все пары чисел в строку через пробел для читаемости
        return " ".join(encrypted)

    def decrypt(self, encrypted_text):
        """
        Дешифрование текста из квадрата Полибия
        Принимает строку с кодами, разделенными пробелами или запятыми
        """
        # Получаем ключ для дешифрования
        key = self.get_decrypt_key()

        # Очищаем текст от лишних символов и разбиваем на коды
        # Удаляем все, кроме цифр и пробелов
        cleaned = re.sub(r"[^\d\s]", "", encrypted_text)

        # Разбиваем на отдельные коды (двузначные числа)
        # Сначала пробуем разбить по пробелам
        if " " in cleaned:
            codes = cleaned.split()
        else:
            # Если пробелов нет, разбиваем по 2 символа
            codes = [
                cleaned[i : i + 2]
                for i in range(0, len(cleaned), 2)
                if len(cleaned[i : i + 2]) == 2
            ]

        decrypted = []
        unknown_codes = set()

        for code in codes:
            if code in key:
                decrypted.append(key[code])
            else:
                decrypted.append("?")
                unknown_codes.add(code)

        if unknown_codes:
            print(f"Предупреждение: следующие коды не найдены в ключе: {unknown_codes}")

        return "".join(decrypted)

    def save_key_to_file(self, filename):
        """Сохранение ключа в файл в читаемом формате"""
        encrypt_key = self.get_encrypt_key()

        with open(filename, "w", encoding="utf-8") as f:
            f.write("КЛЮЧ ШИФРОВАНИЯ (буква -> код):\n")
            f.write("-" * 40 + "\n")
            for char, code in sorted(encrypt_key.items()):
                f.write(f"'{char}' -> {code}\n")

            f.write("\n" + "=" * 40 + "\n")
            f.write("КЛЮЧ ДЕШИФРОВАНИЯ (код -> буква):\n")
            f.write("-" * 40 + "\n")
            decrypt_key = self.get_decrypt_key()
            for code, char in sorted(decrypt_key.items()):
                f.write(f"{code} -> '{char}'\n")


# ===================== ЗАДАНИЕ 2: Частотный анализ для 11 варианта =====================


class FrequencyAnalyzer:
    """Класс для частотного анализа и дешифровки моноалфавитной замены с ручной заменой"""

    def __init__(self):
        """Инициализация с точными индексами частот русского языка"""

        # Точные индексы частот появления букв русского алфавита (из задания)
        self.russian_frequencies = {
            " ": 0.128675,
            "о": 0.096456,
            "и": 0.075312,
            "е": 0.072292,
            "а": 0.064841,
            "н": 0.061820,
            "т": 0.061619,
            "с": 0.051953,
            "р": 0.040677,
            "в": 0.039267,
            "м": 0.029803,
            "л": 0.029400,
            "д": 0.026983,
            "я": 0.026379,
            "к": 0.025977,
            "п": 0.024768,
            "з": 0.015908,
            "ы": 0.015707,
            "ь": 0.015103,
            "у": 0.013290,
            "ч": 0.011679,
            "ж": 0.010673,
            "г": 0.009867,
            "х": 0.008659,
            "ф": 0.007249,
            "й": 0.006847,
            "ю": 0.006847,
            "б": 0.006645,
            "ц": 0.005034,
            "ш": 0.004229,
            "щ": 0.003625,
            "э": 0.002416,
            "ъ": 0.000000,
        }

        # Сортируем буквы по убыванию частоты
        self.russian_letters_by_freq = list(self.russian_frequencies.keys())

        # Для удобства создадим список с частотами в процентах для отображения
        self.russian_frequencies_percent = {
            k: v * 100 for k, v in self.russian_frequencies.items()
        }

        # Цвета для выделения (ANSI коды)
        self.GREEN = "\033[92m"
        self.BOLD = "\033[1m"
        self.END = "\033[0m"

    def calculate_frequencies(self, text):
        """Расчет частот символов в тексте (в виде индексов, сумма = 1)"""
        # Приводим к нижнему регистру
        text_lower = text.lower()

        # Удаляем символы конца строки и возврата каретки
        text_clean = text_lower.replace("\n", "").replace("\r", "")

        # Считаем все символы, включая пробелы, но исключая служебные символы
        total = len(text_clean)

        if total == 0:
            return {}, {}, 0

        # Считаем количество каждого символа
        counter = Counter(text_clean)

        # Вычисляем индексы частот (в долях от 1)
        frequencies = {}
        for char, count in counter.items():
            frequencies[char] = count / total

        # Сортируем по убыванию частоты
        sorted_freq = dict(
            sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_freq, counter, total

    def print_frequencies_comparison(
        self, encrypted_freq, encrypted_counter, total_chars
    ):
        """Вывод сравнения частот символов из текста и эталонных русских частот (без выделения)"""
        print("\n" + "=" * 140)
        print("СРАВНЕНИЕ ЧАСТОТ СИМВОЛОВ (зашифрованный текст vs русский язык)")
        print("=" * 140)
        print(
            "| {:^4} | {:^25} | {:^25} | {:^25} | {:^25} | {:^20} |".format(
                "№",
                "Символ в тексте",
                "Частота в тексте",
                "Символ в русском",
                "Частота в русском",
                "Визуализация",
            )
        )
        print("-" * 140)

        encrypted_items = list(encrypted_freq.items())
        russian_items = list(self.russian_frequencies.items())

        max_freq = max(encrypted_freq.values()) if encrypted_freq else 1

        # Определяем максимальное количество для сравнения
        max_len = max(len(encrypted_items), len(russian_items))

        # Выводим сравнение для всех символов
        for i in range(max_len):
            # Данные из зашифрованного текста
            if i < len(encrypted_items):
                enc_char, enc_freq = encrypted_items[i]
                enc_count = encrypted_counter.get(enc_char, 0)
                enc_freq_percent = enc_freq * 100
                enc_display_char = repr(enc_char) if enc_char == " " else enc_char
                enc_display = f"'{enc_display_char}'"
                enc_freq_display = f"{enc_freq_percent:.3f}% [{enc_count} шт.]"

                # Визуализация на основе частоты в тексте
                stars = int((enc_freq / max_freq) * 30)
                viz = "*" * stars
            else:
                enc_display = "-"
                enc_freq_display = "-"
                viz = ""

            # Данные из русского языка
            if i < len(russian_items):
                rus_char, rus_freq = russian_items[i]
                rus_freq_percent = rus_freq * 100
                rus_display_char = repr(rus_char) if rus_char == " " else rus_char
                rus_display = f"'{rus_display_char}'"
                rus_freq_display = f"{rus_freq_percent:.3f}%"
            else:
                rus_display = "-"
                rus_freq_display = "-"

            print(
                "| {:^4} | {:^25} | {:^25} | {:^25} | {:^25} | {:<20} |".format(
                    i + 1,
                    enc_display,
                    enc_freq_display,
                    rus_display,
                    rus_freq_display,
                    viz,
                )
            )

        print("-" * 140)
        print(f"Всего уникальных символов в тексте: {len(encrypted_freq)}")
        print(f"Всего символов в тексте: {total_chars}")
        print(
            f"Всего букв в русском алфавите (с пробелом): {len(self.russian_frequencies)}"
        )
        print("\nПодсказка: Начните замены с сопоставления самых частых символов")

    def print_commands(self):
        """Вывод списка доступных команд"""
        print("\n" + "=" * 140)
        print("ДОСТУПНЫЕ КОМАНДЫ:")
        print("=" * 140)
        print("  x->y       - заменить символ 'x' на 'y' (например: р->о)")
        print(
            "  x->_       - заменить символ 'x' на ПРОБЕЛ (используйте _ для пробела)"
        )
        print("  show       - показать текущий результат")
        print("  freq       - показать сравнение частот символов")
        print("  list       - показать текущие замены")
        print("  undo       - отменить последнюю замену")
        print("  reset      - сбросить все замены")
        print("  save       - сохранить результат в файл")
        print("  help       - показать это сообщение")
        print("  done       - завершить подбор ключа")
        print("-" * 140)

    def decrypt_with_replacement(self, encrypted_text, replacements):
        """
        Дешифровка текста с учетом замен с выделением цветом только в тексте

        replacements: словарь вида {зашифрованный_символ: исходный_символ}
        """
        decrypted_colored = []
        decrypted_plain = []

        for char in encrypted_text:
            # Пропускаем символы конца строки при подсчете, но сохраняем их в выводе
            if char in ["\n", "\r"]:
                decrypted_colored.append(char)
                decrypted_plain.append(char)
                continue

            char_lower = char.lower()
            if char_lower in replacements:
                # Сохраняем регистр оригинального символа
                if char.isupper():
                    replaced_char = replacements[char_lower].upper()
                else:
                    replaced_char = replacements[char_lower]

                # Для цветного вывода (только в тексте)
                decrypted_colored.append(
                    f"{self.GREEN}{self.BOLD}{replaced_char}{self.END}"
                )
                # Для обычного вывода (сохранение в файл)
                decrypted_plain.append(replaced_char)
            else:
                decrypted_colored.append(char)
                decrypted_plain.append(char)

        return "".join(decrypted_colored), "".join(decrypted_plain)

    def save_results(self, encrypted_text, replacements, variant):
        """Сохранение результатов дешифровки"""
        # Получаем расшифрованный текст (обычный, без цветов)
        _, decrypted_plain = self.decrypt_with_replacement(encrypted_text, replacements)

        # Создаем имя файла с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Сохраняем расшифрованный текст
        text_filename = f"task2_decrypted_var{variant}_{timestamp}.txt"
        with open(text_filename, "w", encoding="utf-8") as f:
            f.write(decrypted_plain)
        print(f"\n✅ Расшифрованный текст сохранен в {text_filename}")

        # Сохраняем ключ
        key_filename = f"task2_key_var{variant}_{timestamp}.txt"
        with open(key_filename, "w", encoding="utf-8") as f:
            f.write("КЛЮЧ ДЕШИФРОВКИ:\n")
            f.write("=" * 40 + "\n")
            f.write("Зашифрованный символ -> Исходный символ\n")
            f.write("-" * 40 + "\n")
            for enc, orig in sorted(replacements.items()):
                orig_display = "_" if orig == " " else orig
                f.write(f"'{enc}' -> '{orig_display}'\n")

            f.write("\n" + "=" * 40 + "\n")
            f.write("Исходный символ -> Зашифрованный символ\n")
            f.write("-" * 40 + "\n")
            # Обратный словарь для удобства
            reverse_key = {v: k for k, v in replacements.items()}
            for orig, enc in sorted(reverse_key.items()):
                orig_display = "_" if orig == " " else orig
                f.write(f"'{orig_display}' -> '{enc}'\n")

        print(f"✅ Ключ дешифровки сохранен в {key_filename}")

        return decrypted_plain

    def interactive_replacement(self, encrypted_text, variant):
        """
        Интерактивный режим замены символов
        Пользователь вводит замены в формате 'x->y'
        """
        replacements = {}  # зашифрованный -> исходный
        history = []  # История замен для отмены

        # Получаем начальные частоты (без учета концов строк)
        frequencies, counter, total_chars = self.calculate_frequencies(encrypted_text)

        print("\n" + "=" * 140)
        print("ИНТЕРАКТИВНЫЙ РЕЖИМ ЗАМЕНЫ СИМВОЛОВ")
        print("=" * 140)

        # Сразу показываем сравнение частот (без выделения)
        self.print_frequencies_comparison(frequencies, counter, total_chars)
        self.print_commands()

        while True:
            # Показываем текущий результат с выделением цветом
            colored_result, plain_result = self.decrypt_with_replacement(
                encrypted_text, replacements
            )
            print("\n" + "=" * 140)
            print("ТЕКУЩИЙ РЕЗУЛЬТАТ (зеленым выделены замененные символы):")
            print("-" * 140)
            print(colored_result)

            if replacements:
                print(
                    "\nТекущие замены:",
                    ", ".join(
                        [
                            f"{k}->{v if v != ' ' else '_'}"
                            for k, v in replacements.items()
                        ]
                    ),
                )

            print("=" * 140)

            command = input("\nВведите команду: ").strip().lower()

            if command == "done":
                # При завершении автоматически сохраняем результаты
                print("\nЗавершение работы. Сохранение результатов...")
                self.save_results(encrypted_text, replacements, variant)
                break

            elif command == "show":
                continue

            elif command == "freq":
                frequencies, counter, total_chars = self.calculate_frequencies(
                    encrypted_text
                )
                self.print_frequencies_comparison(frequencies, counter, total_chars)

            elif command == "list":
                if replacements:
                    print("\nТекущие замены:")
                    for enc, orig in sorted(replacements.items()):
                        orig_display = "_" if orig == " " else orig
                        print(f"  '{enc}' -> '{orig_display}'")
                else:
                    print("\nЗамены не заданы")

            elif command == "undo":
                if history:
                    last = history.pop()
                    del replacements[last]
                    print(f"Отменена замена: '{last}'")
                else:
                    print("Нет замен для отмены")

            elif command == "reset":
                replacements = {}
                history = []
                print("Все замены сброшены")

            elif command == "help":
                self.print_commands()

            elif command == "save":
                # Ручное сохранение
                self.save_results(encrypted_text, replacements, variant)

            elif "->" in command:
                # Парсим команду замены
                parts = command.split("->")
                if len(parts) == 2:
                    enc_char = parts[0].strip()
                    orig_char = parts[1].strip()

                    if len(enc_char) == 1:
                        # Обработка пробела
                        if orig_char == "_":
                            orig_char = " "

                        # Добавляем замену
                        replacements[enc_char] = orig_char
                        history.append(enc_char)

                        # Показываем обновленный результат сразу
                        orig_display = "_" if orig_char == " " else orig_char
                        print(
                            f"\n✅ Добавлена замена: '{enc_char}' -> '{orig_display}'"
                        )
                    else:
                        print("Ошибка: формат должен быть 'x->y' (по одному символу)")
                else:
                    print("Ошибка: неверный формат. Используйте 'x->y'")
            else:
                print("Неизвестная команда. Введите 'help' для списка команд.")


# ===================== ОСНОВНАЯ ПРОГРАММА =====================


def save_to_file(filename, content):
    """Сохранение данных в файл"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Сохранено в {filename}")


def load_from_file(filename):
    """Загрузка данных из файла"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def task1_polybius_square():
    """Выполнение задания 1: шифрование квадратом Полибия"""
    print("\n" + "=" * 140)
    print("ЗАДАНИЕ 1: Шифрование квадратом Полибия")
    print("=" * 140)

    original_text = """информационная безопасность является одной из важнейших задач в современном мире.
с развитием информационных технологий и интернета вопросы защиты данных становятся все более актуальными.
криптография наука о методах шифрования существует уже тысячи лет.
одним из первых известных шифров является шифр цезаря который использовал сдвиг алфавита.
квадрат полибия который мы будем использовать в этой лабораторной работе был изобретен в древней греции.
этот метод шифрования представляет собой квадратную таблицу в которую вписаны буквы алфавита.
каждая буква заменяется парой чисел соответствующих строке и столбцу в которых она находится.
такой метод позволяет достаточно просто шифровать сообщения но при этом обеспечивает некоторую защиту.
в современном мире используются гораздо более сложные алгоритмы шифрования такие как aes и rsa.
однако изучение простых шифров помогает понять базовые принципы криптографии.
шифрование и дешифрование должны работать корректно чтобы можно было восстановить исходное сообщение.
это важно для проверки правильности реализации алгоритма.
в данной лабораторной работе мы изучаем простейшие методы шифрования текстовых сообщений."""

    print(f"Исходный текст (длина: {len(original_text)} символов):")
    print(original_text[:300] + "..." if len(original_text) > 300 else original_text)

    # Сохраняем исходный текст
    save_to_file("task1_original.txt", original_text)

    # Создаем квадрат Полибия
    polybius = PolybiusSquare()
    polybius.print_square()

    # Шифруем текст
    print("\nШифрование текста...")
    encrypted_text = polybius.encrypt(original_text)
    print("\nЗАШИФРОВАННЫЙ ТЕКСТ:")
    print("-" * 50)
    print(encrypted_text[:500] + "..." if len(encrypted_text) > 500 else encrypted_text)

    # Сохраняем зашифрованный текст
    save_to_file("task1_encrypted.txt", encrypted_text)

    # Сохраняем ключ в читаемом формате
    polybius.save_key_to_file("task1_key.txt")
    print("\nКлюч шифрования сохранен в task1_key.txt")

    # Дешифрование
    print("\nДешифрование текста...")
    decrypted_text = polybius.decrypt(encrypted_text)
    print("\nРАСШИФРОВАННЫЙ ТЕКСТ:")
    print("-" * 50)
    print(decrypted_text[:500] + "..." if len(decrypted_text) > 500 else decrypted_text)

    return encrypted_text


def task2_frequency_analysis():
    """Выполнение задания 2: частотный анализ для 11 варианта с загрузкой из code11.txt"""
    print("\n" + "=" * 140)
    print("ЗАДАНИЕ 2: Частотный анализ моноалфавитной замены (вариант 11)")
    print("=" * 140)

    variant = "11"
    filename = "code11.txt"

    # Загружаем текст из файла code11.txt
    print(f"\nЗагрузка зашифрованного текста из файла {filename}...")
    encrypted_text = load_from_file(filename)

    if encrypted_text is None:
        print(f"Файл {filename} не найден.")
        print(
            "Пожалуйста, создайте файл code11.txt с зашифрованным текстом для 11 варианта."
        )
        return

    print(f"Файл {filename} успешно загружен.")

    # Сохраняем загруженный текст в файл для варианта
    output_filename = f"task2_encrypted_var{variant}.txt"
    save_to_file(output_filename, encrypted_text)

    print(f"\nЗашифрованный текст (вариант: {variant}):")
    print("-" * 50)
    print(encrypted_text)

    # Создаем анализатор частот
    analyzer = FrequencyAnalyzer()

    # Интерактивный режим замены
    analyzer.interactive_replacement(encrypted_text, variant)

    print("\nЗадание 2 выполнено!")


def main():
    """Главная функция"""
    print("=" * 140)
    print("ЛАБОРАТОРНАЯ РАБОТА №1")
    print("Простейшие методы шифрования текстовых сообщений")
    print("=" * 140)

    while True:
        print("\nВыберите действие:")
        print("1. Выполнить задание 1 (Квадрат Полибия)")
        print("2. Выполнить задание 2 (Частотный анализ, вариант 11)")
        print("3. Выполнить оба задания")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            task1_polybius_square()
        elif choice == "2":
            task2_frequency_analysis()
        elif choice == "3":
            task1_polybius_square()
            task2_frequency_analysis()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 0.")


if __name__ == "__main__":
    main()

import os
from frequency_analysis import run_frequency_analysis


def get_data_dir():
    """Определяет путь к папке data относительно расположения скрипта"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, "data")


def read_file(filename):
    """Читает содержимое файла из папки data"""
    data_dir = get_data_dir()
    path = os.path.join(data_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save(filename, content):
    """Сохраняет содержимое в файл в папке data"""
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_key(filename):
    """Загружает ключ дешифровки из файла формата: <символ> -> <буква>"""
    data_dir = get_data_dir()
    path = os.path.join(data_dir, filename)
    key = {}
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    ch = parts[0].strip()
                    lt = parts[1].strip()
                    if ch == "[ПРОБЕЛ]":
                        ch = " "
                    if lt == "[ПРОБЕЛ]":
                        lt = " "
                    key[ch] = lt
    return key


def decrypt(text, key):
    """Расшифровывает текст с помощью ключа"""
    return "".join(key.get(c, c) for c in text)


def main():
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 2: ДЕШИФРОВКА (Вариант 15)")
    print("=" * 70)

    data_dir = get_data_dir()
    print(f"\n📂 Рабочая папка: {data_dir}")

    # Чтение зашифрованного текста из файла
    encrypted = read_file("task2_encrypted.txt")
    print(f"📄 Зашифрованный текст загружен ({len(encrypted)} симв.)")

    # === ШАГ 1: ЧАСТОТНЫЙ АНАЛИЗ (вызывается из модуля) ===
    print("\n" + "=" * 70)
    print("ШАГ 1: ЧАСТОТНЫЙ АНАЛИЗ")
    print("=" * 70)

    run_frequency_analysis(encrypted)

    # === ШАГ 2: ЗАГРУЗКА КЛЮЧА ИЗ ФАЙЛА ===
    print("\n" + "=" * 70)
    print("ШАГ 2: ЗАГРУЗКА КЛЮЧА ИЗ ФАЙЛА")
    print("=" * 70)

    decryption_key = load_key("task2_key_input.txt")

    if not decryption_key:
        print(f"\n❌ Ошибка: Файл 'task2_key_input.txt' не найден!")
        print(f"   Путь: {os.path.join(data_dir, 'task2_key_input.txt')}")
        return

    print(f"\n✅ Загружено замен: {len(decryption_key)}")

    # === ШАГ 3: РАСШИФРОВКА ===
    print("\n" + "=" * 70)
    print("ШАГ 3: РАСШИФРОВКА ТЕКСТА")
    print("=" * 70)

    decrypted = decrypt(encrypted, decryption_key)

    save("task2_decrypted.txt", decrypted)

    print(f"\n✅ Результат сохранен:")
    print(f"   - {data_dir}/task2_decrypted.txt")
    print(f"   - {data_dir}/task2_key_input.txt (ключ)")

    print(f"\n📖 РАСШИФРОВАННЫЙ ТЕКСТ ({len(decrypted)} симв.):")
    print("-" * 70)
    print(decrypted)
    print("-" * 70)
    print("\n=== ДЕШИФРОВКА ЗАВЕРШЕНА ===\n")


if __name__ == "__main__":
    main()
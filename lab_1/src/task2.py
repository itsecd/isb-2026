import os
from collections import Counter


def get_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, "data")


def read_file(filename):
    data_dir = get_data_dir()
    path = os.path.join(data_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save(filename, content):
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_key(filename):
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
    return "".join(key.get(c, c) for c in text)


def main():
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 2: ДЕШИФРОВКА (Вариант 15)")
    print("=" * 70)

    data_dir = get_data_dir()
    print(f"\n📂 Рабочая папка: {data_dir}")

    encrypted = read_file("task2_encrypted.txt")
    print(f"📄 Зашифрованный текст загружен ({len(encrypted)} симв.)")

    # === ШАГ 1: ЧАСТОТНЫЙ АНАЛИЗ ===
    print("\n" + "=" * 70)
    print("ШАГ 1: ЧАСТОТНЫЙ АНАЛИЗ")
    print("=" * 70)

    cnt = Counter(encrypted)
    total = sum(cnt.values())
    freq = sorted(cnt.items(), key=lambda x: x[1], reverse=True)

    print(f"\nВсего символов: {total}")
    print(f"Уникальных символов: {len(freq)}\n")
    print(f"{'№':<3} | {'Символ':<10} | {'Кол-во':<8} | {'%':<7}")
    print("-" * 50)

    for i, (ch, count) in enumerate(freq):
        pct = count / total * 100
        ch_display = "[ПРОБЕЛ]" if ch == " " else ch
        print(f"{i + 1:<3} | {ch_display:<10} | {count:<8} | {pct:<7.1f}")

    freq_content = "ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА\n" + "=" * 60 + "\n\n"
    freq_content += f"Всего символов: {total}\nУникальных символов: {len(freq)}\n\n"
    freq_content += f"{'Символ':<12} | {'Кол-во':<10} | {'Частота (%)':<12}\n"
    freq_content += "-" * 60 + "\n"
    for i, (ch, count) in enumerate(freq):
        pct = count / total * 100
        ch_display = "[ПРОБЕЛ]" if ch == " " else ch
        freq_content += f"{ch_display:<12} | {count:<10} | {pct:<12.2f}\n"
    save("task2_frequencies.txt", freq_content)
    print(f"\n✅ Частоты сохранены: {data_dir}/task2_frequencies.txt")

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
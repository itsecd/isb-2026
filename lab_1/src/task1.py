import os
import random

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


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
        if isinstance(content, dict):
            for k, v in content.items():
                k_disp = "[ПРОБЕЛ]" if k == " " else k
                v_disp = "[ПРОБЕЛ]" if v == " " else v
                f.write(f"{k_disp} -> {v_disp}\n")
        else:
            f.write(content)


def generate_key():
    """Генерирует случайный ключ шифрования"""
    shuffled = list(ALPHABET)
    random.shuffle(shuffled)
    return {orig: sub for orig, sub in zip(ALPHABET, shuffled)}


def process_text(text, key):
    """Шифрует или расшифровывает текст"""
    result = []
    for char in text:
        char_upper = char.upper()
        if char_upper in key:
            result.append(key[char_upper])
        else:
            result.append(char)
    return "".join(result)


def main():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 1: ШИФРОВАНИЕ ТЕКСТА")
    print("=" * 60)

    text = read_file("task1_source.txt")
    print(f"\n📄 Исходный текст загружен из файла ({len(text)} симв.)")

    key = generate_key()
    encrypted = process_text(text, key)
    decrypted = process_text(encrypted, {v: k for k, v in key.items()})

    save("task1_encrypted.txt", encrypted)
    save("task1_key.txt", key)
    save("task1_decrypted.txt", decrypted)

    if text.strip().upper() == decrypted.strip().upper():
        print(f"\n✅ Текст зашифрован и проверен")
        print(f"📂 Файлы сохранены в: {get_data_dir()}")
    else:
        print(f"\n❌ Ошибка расшифровки!")


if __name__ == "__main__":
    main()
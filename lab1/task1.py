import random
import os

# === Настройки ===
ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "  # 33 символа: 32 буквы + пробел
assert len(ALPHABET) == 33, "Алфавит должен содержать ровно 33 символа!"

def generate_key():
    """Генерирует случайную моноалфавитную подстановку для ALPHABET."""
    shuffled = list(ALPHABET)
    random.shuffle(shuffled)
    return dict(zip(ALPHABET, shuffled))

def encrypt(text, key):
    """Шифрует текст по ключу. Текст должен быть в верхнем регистре и содержать только символы из ALPHABET."""
    result = []
    for char in text:
        if char in key:
            result.append(key[char])
        else:
            # Если символ не в алфавите (например, знаки), оставляем как есть (на всякий случай)
            result.append(char)
    return "".join(result)

def decrypt(text, key):
    """Расшифровывает текст по ключу."""
    inv_key = {v: k for k, v in key.items()}
    result = []
    for char in text:
        if char in inv_key:
            result.append(inv_key[char])
        else:
            result.append(char)
    return "".join(result)

# === Основной блок ===
if __name__ == "__main__":
    # 1. Чтение исходного текста
    source_path = os.path.join("lab_1", "source_text.txt")
    try:
        with open(source_path, "r", encoding="utf-8") as f:
            original = f.read().upper().replace("Ё", "Е")
        # Удаляем всё, кроме букв и пробелов
        original = "".join(c for c in original if c in ALPHABET)
        if len(original) < 500:
            raise ValueError(f"Текст слишком короткий: {len(original)} символов. Нужно ≥500.")
    except FileNotFoundError:
        print(f"Файл {source_path} не найден. Создайте его вручную с текстом ≥500 символов.")
        exit(1)

    # 2. Генерируем ключ
    key = generate_key()

    # 3. Шифруем
    encrypted = encrypt(original, key)

    # 4. Дешифруем для проверки
    decrypted = decrypt(encrypted, key)

    # 5. Сохраняем результаты
    lab_dir = "lab_1"
    os.makedirs(lab_dir, exist_ok=True)

    with open(os.path.join(lab_dir, "encrypted_task1.txt"), "w", encoding="utf-8") as f:
        f.write(encrypted)

    with open(os.path.join(lab_dir, "decrypted_task1.txt"), "w", encoding="utf-8") as f:
        f.write(decrypted)

    with open(os.path.join(lab_dir, "key_task1.txt"), "w", encoding="utf-8") as f:
        f.write("Символ -> Зашифрованный\n")
        for orig, enc in sorted(key.items()):
            f.write(f"{orig} -> {enc}\n")

    print("✅ Задание 1 выполнено.")
    print(f"Исходный текст: {len(original)} символов")
    print(f"Тексты совпадают? {original == decrypted}")

import random
import os
from typing import Optional

class SubstitutionCipher:
    """Класс для шифрования и дешифрования текста методом простой подстановки."""
    def __init__(self, key: Optional[str] = None) -> None:
        """Инициализация шифра подстановки."""
        self.alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
        if key:
            self.key = key
        else:
            # Генерация случайного ключа
            key_list = list(self.alphabet)
            random.shuffle(key_list)
            self.key = "".join(key_list)

    def encrypt(self, text: str) -> str:
        """Шифрует открытый текст."""
        text = text.upper().replace('Ё', 'Е')
        # Оставляем только символы нашего алфавита
        text = ''.join(c for c in text if c in self.alphabet)
        mapping = str.maketrans(self.alphabet, self.key)
        return text.translate(mapping)

    def decrypt(self, text: str) -> str:
        """Дешифрует зашифрованный текст."""
        mapping = str.maketrans(self.key, self.alphabet)
        return text.translate(mapping)

def main() -> None:
    """ Основная функция для вызова методов"""
    cipher = SubstitutionCipher()

    # Сохраняем сгенерированный ключ
    with open('lab1/data/task1_key.txt', 'w', encoding='utf-8') as f:
        f.write(cipher.key)
    print(f"Сгенерирован ключ: {cipher.key}")

    # Чтение исходного текста
    try:
        with open('lab1/data/task1_source.txt', 'r', encoding='utf-8') as f:
            source_text = f.read()
    except FileNotFoundError:
        print("Создайте файл lab1/data/task1_source.txt с текстом (не менее 500 символов)!")
        return

    # Шифрование
    encrypted_text = cipher.encrypt(source_text)
    with open('lab1/data/task1_encoded.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
    
    # Дешифрование для проверки
    decrypted_text = cipher.decrypt(encrypted_text)
    with open('lab1/data/task1_decoded.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)

    print("Задание 1 успешно выполнено. Результаты сохранены в папке data/")

if __name__ == "__main__":
    main()
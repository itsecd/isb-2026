import json
import random

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
SOURCE_TEXT = (
    "В ЛАБОРАТОРНОЙ РАБОТЕ ИЗУЧАЕТСЯ МЕТОД КОДИРОВАНИЯ ТЕКСТА ШИФРОМ ПРОСТОЙ ПОДСТАНОВКИ И ДЕКОДИРОВАНИЯ "
    "ПРИ ПОМОЩИ ЧАСТОТНОГО АНАЛИЗА ТЕКСТОВОЙ ПОСЛЕДОВАТЕЛЬНОСТИ. "
    "ДЛЯ ПЕРВОГО ЗАДАНИЯ ИСПОЛЬЗУЕТСЯ СВЯЗНЫЙ ТЕКСТ ОБЪЕМОМ БОЛЕЕ ПЯТИСОТ СИМВОЛОВ, ЧТОБЫ МОЖНО БЫЛО "
    "ПРОВЕРИТЬ РАБОТУ АЛГОРИТМА ШИФРОВАНИЯ И ОБРАТНОГО ПРЕОБРАЗОВАНИЯ. "
    "ПРОГРАММА ДОЛЖНА СОХРАНЯТЬ ИСХОДНЫЙ ТЕКСТ, РЕЗУЛЬТАТ ШИФРОВАНИЯ И КЛЮЧ ПОДСТАНОВКИ В ОТДЕЛЬНЫЕ ФАЙЛЫ. "
    "ПОСЛЕ ЭТОГО ВЫПОЛНЯЕТСЯ ОБРАТНОЕ ПРЕОБРАЗОВАНИЕ, КОТОРОЕ ДОЛЖНО ВОССТАНАВЛИВАТЬ ИСХОДНОЕ СООБЩЕНИЕ БЕЗ "
    "ПОТЕРИ СИМВОЛОВ. ТАКЖЕ В РАМКАХ ЛАБОРАТОРНОЙ РАБОТЫ НУЖНО ПОСТРОИТЬ ТАБЛИЦУ ЧАСТОТ ДЛЯ ШИФРОТЕКСТА "
    "И ПОЛУЧИТЬ ЧЕРНОВОЙ РЕЗУЛЬТАТ ДЕШИФРОВАНИЯ МЕТОДОМ ЧАСТОТНОГО АНАЛИЗА."
)

def generate_key():
    rng = random.Random(22)
    shuffled = rng.sample(list(ALPHABET), len(ALPHABET))
    return dict(zip(ALPHABET, shuffled))

def encrypt(text, key):
    return "".join(key.get(ch, ch) for ch in text)

def main():
    key = generate_key()
    cipher = encrypt(SOURCE_TEXT, key)

    with open("orig.txt", "w", encoding="utf-8") as f:
        f.write(SOURCE_TEXT)

    with open("cipher.txt", "w", encoding="utf-8") as f:
        f.write(cipher)

    with open("key.txt", "w", encoding="utf-8") as f:
        json.dump(key, f, ensure_ascii=False, indent=2)

    print("Готово: orig.txt, cipher.txt, key.txt")

if __name__ == "__main__":
    main()
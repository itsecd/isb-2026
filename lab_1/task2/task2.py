import os
from collections import Counter
from typing import List, Tuple, Dict
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import REFERENCE_ORDER, DECRYPTED_TEXT

def load_text(filename: str) -> str:
    """Загружает текст из файла."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def count_frequencies(text: str) -> Tuple[List[Tuple[str, float]], Counter]:
    """Подсчитывает частоты символов, возвращает список (символ, процент) и счётчик."""
    counter: Counter = Counter(text)
    total: int = len(text)
    freq_list: List[Tuple[str, float]] = [(ch, count / total) for ch, count in counter.most_common()]
    return freq_list, counter

def save_frequencies(freq_list: List[Tuple[str, float]], filename: str) -> None:
    """Сохраняет таблицу частот в файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Частоты символов в зашифрованном тексте:\n")
        for ch, perc in freq_list:
            if ch == ' ':
                ch_disp: str = 'пробел'
            else:
                ch_disp = ch
            f.write(f"{ch_disp}: {perc:.4f}\n")

def initial_mapping(freq_list: List[Tuple[str, float]]) -> Dict[str, str]:
    """Строит начальное отображение, сопоставляя самые частые символы с эталонными."""
    mapping: Dict[str, str] = {}
    for i, (ch, _) in enumerate(freq_list):
        if i < len(REFERENCE_ORDER):
            mapping[ch] = REFERENCE_ORDER[i]
        else:
            mapping[ch] = '?'  # на случай лишних символов
    return mapping

def apply_mapping(text: str, mapping: Dict[str, str]) -> str:
    """Применяет текущий ключ к тексту."""
    return ''.join(mapping.get(ch, ch) for ch in text)

def save_key(mapping: Dict[str, str], filename: str) -> None:
    """Сохраняет ключ в файл (enc_char-dec_char)."""
    with open(filename, 'w', encoding='utf-8') as f:
        for enc, dec in mapping.items():
            f.write(f"{enc}-{dec}\n")

def interactive_mode(text: str, mapping: Dict[str, str]) -> None:
    """Интерактивный режим уточнения ключа."""
    print("Интерактивный режим. Вводите замены в формате 'символ-буква'")
    print("Доступные команды: show, save, exit")
    while True:
        cmd: str = input("> ").strip()
        if cmd.lower() == 'show':
            decrypted: str = apply_mapping(text, mapping)
            preview: str = decrypted[:500] + "..." if len(decrypted) > 500 else decrypted
            print("Текущий расшифрованный текст:")
            print(preview)
        elif cmd.lower() == 'save':
            decrypted = apply_mapping(text, mapping)
            with open(DECRYPTED_TEXT, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            save_key(mapping, 'decryption_key.txt')
            print("Результаты сохранены в decrypted.txt и decryption_key.txt")
            break
        elif cmd.lower() == 'exit':
            print("Выход без сохранения.")
            break
        elif '-' in cmd:
            parts: List[str] = cmd.split('-', 1)
            enc_char: str = parts[0].strip()
            dec_char: str = parts[1]
            if len(enc_char) != 1 or len(dec_char) != 1:
                print("Ошибка: вводите по одному символу")
                continue
            mapping[enc_char] = dec_char
            print(f"Замена {enc_char} -> {dec_char} добавлена. Текущий текст:")
            decrypted = apply_mapping(text, mapping)
            preview = decrypted[:500] + "..." if len(decrypted) > 500 else decrypted
            print(preview)
        else:
            print("Неизвестная команда")

def main() -> None:
    cipher_path: str = 'cod9.txt'
    if not os.path.exists(cipher_path):
        print(f"Ошибка: {cipher_path} не найден. Поместите зашифрованный текст в этот файл.")
        return

    ciphertext: str = load_text(cipher_path)
    freq_list, _ = count_frequencies(ciphertext)
    save_frequencies(freq_list, 'frequencies.txt')
    print("Частоты сохранены в frequencies.txt")

    mapping: Dict[str, str] = initial_mapping(freq_list)
    print("Начальное приближение (автоматическое сопоставление по частотам):")
    decrypted: str = apply_mapping(ciphertext, mapping)
    preview: str = decrypted[:500] + "..." if len(decrypted) > 500 else decrypted
    print(preview)
    print("Переходим в интерактивный режим для уточнения.")
    interactive_mode(ciphertext, mapping)

if __name__ == '__main__':
    main()
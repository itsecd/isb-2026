import os
import argparse
from key import KEY

FREQ_FILE: str = "freq.txt"

def parse_args() -> argparse.Namespace:
    """Принимает путь для зашифрованного и расшифрованного текста."""
    parser = argparse.ArgumentParser(
        description="Дешифратор текста методом частного аналза. Пример: py decrypt.py --input code.txt --output text.txt"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help='Путь к файлу с зашифрованным текстом'
    )
    parser.add_argument(
        "--output",
        type=str,
    
        help='Путь к файлу для расшифрованного текста'
    )
    
    return parser.parse_args()

def decrypt(text: str, filename: str) -> None:
    """Дешифратор"""
    dec_text = ""
    
    for el in text:
        if el in KEY:
            dec_text += KEY[el]
        else:            
            dec_text += el
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(dec_text)


def get_freq(text: str) -> dict[str, float]:
    """Функция для подсчета частоты"""
    symbols = set(text.strip())
    freq = {}
    
    for el in symbols:
        if el != "\n":
            freq[el] = round(text.count(el) / len(text), 6)

    return dict(sorted(freq.items(), key=lambda it: it[1], reverse=True))

def save_freq(filename: str, freq_dict: dict[str, float]) -> None:
    """Функция для сохранения подсчетов частоты"""
    with open(filename, "w", encoding="utf-8") as f:
        for (key, val) in freq_dict.items():
            f.writelines(key + " : " + str(val) + "\n")



def main() -> None:
    
    args = parse_args()
    text_path, dec_path = args.input, args.output
    
    if not os.path.exists(text_path):
        print(f"Error: {text_path} файл не найден.")
        return

    with open(text_path, "r", encoding="utf-8") as file:
        text: str = file.read()
    
    freq = get_freq(text)
    save_freq(FREQ_FILE, freq)
    decrypt(text, dec_path)
    
    with open(dec_path, 'r', encoding='utf-8') as file:
        content: str = file.read()
        
    print("Расшифровка завершена.")
    print(f"Результат сохранен в: {dec_path}")
    print("-" * 30)
    print("Output:")
    print(content)
    print("-" * 30)


if __name__ == "__main__":
    main()
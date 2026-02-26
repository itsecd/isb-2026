import argparse
import sys
import os

def parse_args() -> argparse.Namespace:
    """Настраивает и возвращает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="""Шифрование/Дешифрование Атбаш с использованием внешних файлов. 
        Пример: py Base_IB1.py --key key.txt --input orig.txt --output encrypted.txt
        (--input encrypted.txt --output decrypted.txt) для расшифровки условно
        """
    )
    parser.add_argument(
        '--key', 
        required=True, 
        help="Путь к файлу с ключом (алфавитом)"
    )
    parser.add_argument(
        '--input', 
        required=True, 
        help="Путь к входному файлу с текстом. Сюда указывать файл для шифровки/дешифровки"
    )
    parser.add_argument(
        '--output', 
        required=True, 
        help="Путь к выходному файлу для результата"
    )
    
    return parser.parse_args()

def load_key(key_file_path: str) -> str:
    """Загружает алфавит из файла ключа."""
    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"Файл ключа не найден: {key_file_path}")
    
    with open(key_file_path, 'r', encoding='utf-8') as f:
        key_content = f.read().strip()
    
    if len(key_content) < 2:
        raise ValueError("Файл ключа слишком короткий или пуст.")
    
    return key_content

def load_text(text_file_path: str) -> str:
    """Загружает текст для обработки."""
    if not os.path.exists(text_file_path):
        raise FileNotFoundError(f"Файл текста не найден: {text_file_path}")
    
    with open(text_file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_text(text: str, output_file_path: str) -> None:
    """Сохраняет результат в файл."""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def atbash_cipher(text: str, key_alphabet: str) -> str:

    half_len = len(key_alphabet) // 2
    lower_alpha = key_alphabet[:half_len]
    upper_alpha = key_alphabet[half_len:]
    
    rev_lower = lower_alpha[::-1]
    rev_upper = upper_alpha[::-1]
    
    trans_table = str.maketrans(
        lower_alpha + upper_alpha,
        rev_lower + rev_upper
    )
    
    return text.translate(trans_table)

def main():
    args = parse_args()
    
    try:
        key_alphabet = load_key(args.key) #ключ
        
        original_text = load_text(args.input) #ориг текст
        
        result_text = atbash_cipher(original_text, key_alphabet) #шифровка
        
        save_text(result_text, args.output) # сохранение результата
        
        print(f"Входной файл: {args.input}")
        print(f"Файл ключа: {args.key}")
        print(f"Результат сохранен в: {args.output}")
        
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

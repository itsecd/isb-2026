import os
import ast
from frequency import analyze, make_freq_table
from utils import read_file, write_file, clear_screen

def decrypt_task():
    """Расшифровка текста с использованием ключа замены."""
    clear_screen()
    print("="*60)
    print("ЗАДАНИЕ 2: РАСШИФРОВКА ПО КЛЮЧУ")
    print("="*60)
    
    os.makedirs("texts", exist_ok=True)
    os.makedirs("keys", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    filename = input("Введите имя файла с текстом: ").strip()
    text_path = f"texts/{filename}"
    
    cipher_text = read_file(text_path)
    if not cipher_text:
        return
    
    print(f"Загружено {len(cipher_text)} символов")
    
    key_path = input("Введите имя файла с ключом: ").strip()
    if not os.path.exists(key_path):
        key_path = f"keys/{key_path}"
    
    key_content = read_file(key_path)
    if not key_content:
        return
    
    try:
        decrypt_key = ast.literal_eval(key_content)
        print(f"Загружен ключ с {len(decrypt_key)} заменами")
    except:
        print("Ошибка: файл ключа должен содержать словарь Python")
        return
    
    plain_text = ""
    for char in cipher_text:
        plain_text += decrypt_key.get(char, char)
    
    print("\nРЕЗУЛЬТАТ (первые 500 символов):")
    print("-"*60)
    print(plain_text[:500])
    
    name = filename.replace('.txt', '')
    out_dir = f"results/{name}"
    os.makedirs(out_dir, exist_ok=True)
    
    counter, _ = analyze(cipher_text)
    total = len(cipher_text)
    freq_table = make_freq_table(counter, total)
    write_file(f"{out_dir}/frequency_table.txt", freq_table)
    write_file(f"{out_dir}/decrypted.txt", plain_text)
    write_file(f"{out_dir}/key.txt", key_content)
    
    print(f"\nРезультаты сохранены в папке: {out_dir}")
    input("\nНажмите Enter...")

def main():
    """Главное меню программы расшифровки."""
    while True:
        clear_screen()
        print("="*60)
        print("ЗАДАНИЕ 2: РАСШИФРОВКА ТЕКСТА")
        print("="*60)
        print("\n1. Расшифровать текст по ключу")
        print("2. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            decrypt_task()
        elif choice == '2':
            break
        else:
            print("Неверный выбор")
            input("\nНажмите Enter...")

if __name__ == "__main__":
    main()

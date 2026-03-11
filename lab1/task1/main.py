# -*- coding: utf-8 -*-
# main.py

import os
from polybius import PolybiusSquare
from utils import read_file, write_file, clear_screen

def encrypt_task():
    """Задача шифрования: чтение файла, шифрование и сохранение результатов."""
    clear_screen()
    print("="*50)
    print(" ШИФРОВАНИЕ КВАДРАТОМ ПОЛИБИЯ")
    print("="*50)
    
    os.makedirs("texts", exist_ok=True)
    
    filename = input("Введите имя файла (например, my_text.txt): ").strip()
    filepath = f"texts/{filename}"
    
    text = read_file(filepath)
    if not text:
        return
    
    print(f" Загружено {len(text)} символов")
    
    poly = PolybiusSquare("square.txt")
    poly.show()
    
    encrypted = poly.encrypt(text)
    decrypted = poly.decrypt(encrypted)
    
    print(f"\n Зашифровано: {encrypted[:200]}...")
    
    text_upper = text.upper()
    is_correct = (text_upper == decrypted)
    print(f"\n Проверка: {is_correct}")
    
    name = filename.replace('.txt', '')
    out_dir = f"results/{name}"
    os.makedirs(out_dir, exist_ok=True)
    
    write_file(f"{out_dir}/original.txt", text)
    write_file(f"{out_dir}/encrypted.txt", encrypted)
    write_file(f"{out_dir}/decrypted_check.txt", decrypted)
    
    print(f"\n Результаты: {out_dir}")
    input("\nНажмите Enter...")

def decrypt_task():
    """Задача расшифровки: чтение зашифрованного файла и дешифрование."""
    clear_screen()
    print("="*50)
    print(" РАСШИФРОВКА")
    print("="*50)
    
    enc_file = input("Файл с зашифрованным текстом: ").strip()
    
    text = read_file(enc_file)
    if not text:
        return
    
    poly = PolybiusSquare("square.txt")
    poly.show()
    
    decrypted = poly.decrypt(text)
    
    print("\n Результат:")
    print("-"*40)
    print(decrypted[:300])
    
    out_file = f"results/decrypted_{os.path.basename(enc_file)}"
    write_file(out_file, decrypted)
    
    input("\nНажмите Enter...")

def main():
    """Главное меню программы."""
    while True:
        clear_screen()
        print("="*50)
        print("ЗАДАНИЕ 1: КВАДРАТ ПОЛИБИЯ")
        print("="*50)
        print("\n1.  Зашифровать текст")
        print("2.  Расшифровать текст")
        print("3.  Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            encrypt_task()
        elif choice == '2':
            decrypt_task()
        elif choice == '3':
            print("\n До свидания!")
            break
        else:
            print(" Неверный выбор")
            input("\nНажмите Enter...")

if __name__ == "__main__":
    main()

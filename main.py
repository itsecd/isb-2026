#!/usr/bin/env python3
"""
Гибридная криптосистема с использованием RSA и Camellia
Лабораторная работа №3 "Основы Информационной Безопасности"

Данная программа реализует гибридную криптосистему:
- Асимметричное шифрование: RSA (2048 бит) для обмена ключами
- Симметричное шифрование: Camellia (256 бит, режим CBC) для шифрования данных

Режимы работы:
1. Генерация ключей - создание RSA пары и симметричного ключа
2. Шифрование данных - шифрование файла с использованием гибридной схемы
3. Дешифрование данных - расшифровка файла
4. Настройка путей - изменение конфигурации файлов
"""

import argparse
import os
import sys
from typing import Dict, NoReturn

from src.config import manage_settings, HELP_DESCRIPTION, HELP_EPILOG
from src.key_generator import run_key_generation
from src.encryptor import run_encryption
from src.decryptor import run_decryption


def create_directories() -> None:
    """
    Создание необходимых директорий для работы программы.
    
    Создаёт директории 'data' и 'keys' в корне проекта,
    если они не существуют. Эти директории используются для
    хранения входных/выходных файлов и ключей соответственно.
    
    Returns:
        None
    
    Example:
        >>> create_directories()
        # Создаст папки data/ и keys/ если их нет
    """
    for d in ['data', 'keys']:
        os.makedirs(d, exist_ok=True)


def configure_paths(settings: Dict[str, str]) -> Dict[str, str]:
    """
    Настройка путей к файлам в интерактивном режиме.
    
    Позволяет пользователю интерактивно изменить текущие настройки путей.
    Для каждого параметра отображается текущее значение, пользователь может
    ввести новое или оставить старое, нажав Enter.
    
    Args:
        settings (Dict[str, str]): Текущий словарь с настройками,
            где ключ - имя параметра, значение - путь к файлу
    
    Returns:
        Dict[str, str]: Обновлённый словарь с настройками
    
    Example:
        >>> settings = {'initial_file': 'data/plaintext.txt'}
        >>> settings = configure_paths(settings)
        # Пользователь вводит новое значение или оставляет старое
    """
    print("\n Настройка путей ")
    print("Текущие значения (Enter - оставить без изменений):")
    
    for key in settings.keys():
        new_value = input(f"  {key} [{settings[key]}]: ").strip()
        if new_value:
            settings[key] = new_value
    
    manage_settings(settings)
    return settings


def print_menu() -> None:
    """
    Вывод главного меню интерактивного режима.
    
    Отображает доступные режимы работы программы с нумерацией:
    1 - Генерация ключей
    2 - Шифрование данных
    3 - Дешифрование данных
    4 - Настройка путей
    0 - Выход
    
    Returns:
        None
    """
    print("\n" + "="*60)
    print("Гибридная система (RSA + Camellia)")
    print("Лабораторная работа №3")
    print("="*60)
    print("\nРежимы работы:")
    print("  1 - Генерация ключей ")
    print("  2 - Шифрование данных ")
    print("  3 - Дешифрование данных ")
    print("  4 - Настройка путей")
    print("  0 - Выход")
    print("-"*60)


def interactive_mode() -> None:
    """
    Интерактивный режим работы программы.
    
    Запускает бесконечный цикл с меню, позволяющий пользователю:
    - Генерировать ключи (режим 1)
    - Шифровать данные (режим 2)
    - Дешифровать данные (режим 3)
    - Настраивать пути к файлам (режим 4)
    - Выходить из программы (режим 0)
    
    Перед выполнением операций проверяет наличие необходимых файлов
    и выводит информационные сообщения о ходе выполнения.
    
    Returns:
        None
    
    Raises:
        KeyError: Если в настройках отсутствуют необходимые ключи
    """
    create_directories()
    settings = manage_settings()
    
    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()
        
        match choice:
            case '1':
                print("\n Генерация ключей ")
                run_key_generation(
                    public_key_path=settings['public_key'],
                    private_key_path=settings['private_key'],
                    symmetric_key_path=settings['symmetric_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '2':
                print("\n Шифрование данных")
                if not os.path.exists(settings['encrypted_symmetric_key']):
                    print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                    print("Сначала выполните режим 1 (Генерация ключей).")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                run_encryption(
                    input_file=settings['initial_file'],
                    private_key_path=settings['private_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                    output_file=settings['encrypted_file']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '3':
                print("\n Дешифрование данных")
                if not os.path.exists(settings['encrypted_symmetric_key']):
                    print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                if not os.path.exists(settings['encrypted_file']):
                    print(f"\n Зашифрованный файл не найден: {settings['encrypted_file']}")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                run_decryption(
                    encrypted_file=settings['encrypted_file'],
                    private_key_path=settings['private_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                    output_file=settings['decrypted_file']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '4':
                settings = configure_paths(settings)
            
            case '0':
                print("\nДо свидания!")
                break
            
            case _:
                print("\n Неверный выбор. Пожалуйста, выберите 0-4.")
                input("Нажмите Enter для продолжения...")


def main() -> None:
    """
    Основная функция программы.
    
    Обрабатывает аргументы командной строки и запускает соответствующие режимы.
    
    Поддерживаемые аргументы:
        --interactive           - запуск интерактивного меню
        --gen                   - генерация ключей
        --enc                   - шифрование данных
        --dec                   - дешифрование данных
        --public KEY_PATH       - путь к публичному ключу RSA
        --private KEY_PATH      - путь к приватному ключу RSA
        --symmetric KEY_PATH    - путь к симметричному ключу
        --encrypted-symmetric PATH - путь к зашифрованному симметричному ключу
        --input, -i FILE        - входной файл
        --output, -o FILE       - выходной файл
    
    Приоритет аргументов командной строки выше, чем настроек из settings.json.
    Если аргументы не указаны, запускается интерактивный режим.
    
    Returns:
        None
    
    Examples:
        >>> # Генерация ключей
        >>> python main.py --gen --public keys/public.pem --private keys/private.pem
        
        >>> # Шифрование файла
        >>> python main.py --enc --input data/plaintext.txt --output data/encrypted.bin
        
        >>> # Дешифрование файла
        >>> python main.py --dec --input data/encrypted.bin --output data/decrypted.txt
        
        >>> # Интерактивный режим
        >>> python main.py --interactive
        >>> python main.py  # тоже запускает интерактивный режим
    """
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--interactive', action='store_true', help='Интерактивный режим')
    parser.add_argument('--gen', action='store_true', help='Генерация ключей')
    parser.add_argument('--enc', action='store_true', help='Шифрование')
    parser.add_argument('--dec', action='store_true', help='Дешифрование')
    
    parser.add_argument('--public', dest='public_key', help='Открытый ключ RSA')
    parser.add_argument('--private', dest='private_key', help='Закрытый ключ RSA')
    parser.add_argument('--symmetric', dest='symmetric_key', help='Симметричный ключ')
    parser.add_argument('--encrypted-symmetric', dest='encrypted_symmetric_key', help='Зашифрованный симметричный ключ')
    parser.add_argument('--input', '-i', help='Входной файл')
    parser.add_argument('--output', '-o', help='Выходной файл')
    
    args = parser.parse_args()
    
    create_directories()
    settings = manage_settings()
    
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    match True:
        case _ if args.gen:
            public = args.public_key or settings['public_key']
            private = args.private_key or settings['private_key']
            symmetric = args.symmetric_key or settings['symmetric_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_key_generation(public, private, symmetric, encrypted_sym)
        
        case _ if args.enc:
            input_file = args.input or settings['initial_file']
            output_file = args.output or settings['encrypted_file']
            private = args.private_key or settings['private_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_encryption(input_file, private, encrypted_sym, output_file)
        
        case _ if args.dec:
            input_file = args.input or settings['encrypted_file']
            output_file = args.output or settings['decrypted_file']
            private = args.private_key or settings['private_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_decryption(input_file, private, encrypted_sym, output_file)
        
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
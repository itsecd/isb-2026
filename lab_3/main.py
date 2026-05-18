import argparse

from AES import aes_decrypt, aes_encrypt
from key_gen import generate_and_save_keys
from utils import save_settings, load_settings


def get_config_path():
    """
    Парсит аргументы командной строки и возвращает путь до файла конфигурации.

    """
    parser = argparse.ArgumentParser(
        description="Получение пути до файла настроек"
    )
    parser.add_argument(
        '-c', '--config',
        help="Путь до файла с настройками",
        default="settings.json",
    )
    args = parser.parse_args()
    return args.config


def generating(settings: dict):
    """
    Работа с пользователем при генерации ключей

    Args:
        settings (dict): словарь с настройками
    """
    while True:
        print(f"[1] Путь к симметричному ключу: {settings['symmetric_key']}\n[2] Путь к публичному ключу: {settings['public_key']}\n[3] Путь к приватному ключу: {settings['private_key']}\n[4] Длина ключа (128, 192, 256): {settings['lenght']}")
        print("[5] Сгенерировать\n[0] - Выход")
        try:
            choice = int(input())
            match choice:
                case 1:
                    settings['symmetric_key'] = input("Введите путь для сохранения симметричного ключа: ")
                case 2:
                    settings['public_key'] = input("Введите путь для сохранения публичного ключа: ")
                case 3:
                    settings['private_key'] = input("Введите путь для сохранения приватного ключа: ")
                case 4:
                    settings['lenght'] = int(input("Введите длину ключа (128, 192, 256): "))
                case 5:
                    if settings['lenght'] not in (128, 192, 256) or settings['symmetric_key'] == "" or settings['public_key'] == "" or settings['private_key'] == "":
                        print("Установлены не все требуемые параметры или они некорректны")
                        continue
                    try:
                        generate_and_save_keys(settings['lenght'], settings['public_key'], settings['private_key'], settings['symmetric_key'])
                    except PermissionError:
                        continue
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        print(e)
                        continue
                    print("Ключи сгенерированы и сохранены в файлы!")
                case 0:
                    save_settings(settings)
                    return
                case _:
                    print("Указан неверный режим...\n")
                    continue
        except ValueError:
            print("Ошибка ввода...\n")
            continue
        except PermissionError:
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(e)
            continue


def encrypting(settings: dict):
    """
    Работа с пользователем при шифровании

    Args:
        settings (dict): словарь с настройками
    """
    while True:
        print(f"[1] Путь к симметричному ключу: {settings['symmetric_key']}\n[2] Путь к приватному ключу: {settings['private_key']}\n[3] Путь к исходному файлу: {settings['initial_file']}\n[4] Путь к зашифрованному файлу: {settings['encrypted_file']}")
        print("[5] Зашифровать\n[0] - Выход")
        try:
            choice = int(input())
            match choice:
                case 1:
                    settings['symmetric_key'] = input("Введите путь к симметричному ключу: ")
                case 2:
                    settings['private_key'] = input("Введите путь к приватному ключу: ")
                case 3:
                    settings['initial_file'] = input("Введите путь к исходному файлу: ")
                case 4:
                    settings['encrypted_file'] = input("Введите путь для сохранения зашифрованного файла: ")
                case 5:
                    if settings['encrypted_file'] == "" or settings['symmetric_key'] == "" or settings['private_key'] == "" or settings['initial_file'] == "":
                        print("Установлены не все требуемые параметры или они некорректны")
                        continue
                    try:
                        aes_encrypt(settings['initial_file'], settings['private_key'], settings['symmetric_key'], settings['encrypted_file'])
                    except PermissionError:
                        continue
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        print(e)
                        continue
                    print("Файл успешно зашифрован!")
                case 0:
                    save_settings(settings)
                    return
                case _:
                    print("Указан неверный режим...\n")
                    continue
        except ValueError:
            print("Ошибка ввода...\n")
            continue
        except PermissionError:
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(e)
            continue


def decrypting(settings: dict):
    """
    Работа с пользователем при расшифровке

    Args:
        settings (dict): словарь с настройками
    """
    while True:
        print(f"[1] Путь к симметричному ключу: {settings['symmetric_key']}\n[2] Путь к приватному ключу: {settings['private_key']}\n[3] Путь к расшифрованному файлу: {settings['decrypted_file']}\n[4] Путь к зашифрованному файлу: {settings['encrypted_file']}")
        print("[5] Расшифровать\n[0] - Выход")
        try:
            choice = int(input())
            match choice:
                case 1:
                    settings['symmetric_key'] = input("Введите путь к симметричному ключу: ")
                case 2:
                    settings['private_key'] = input("Введите путь к приватному ключу: ")
                case 3:
                    settings['decrypted_file'] = input("Введите путь куда сохранить расшифровку: ")
                case 4:
                    settings['encrypted_file'] = input("Введите путь к зашифрованному файлу: ")
                case 5:
                    if settings['encrypted_file'] == "" or settings['symmetric_key'] == "" or settings['private_key'] == "" or settings['decrypted_file'] == "":
                        print("Установлены не все требуемые параметры или они некорректны")
                        continue
                    try:
                        aes_decrypt(settings['encrypted_file'], settings['private_key'], settings['symmetric_key'], settings['decrypted_file'])
                    except PermissionError:
                        continue
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        print(e)
                        continue
                    print("Файл успешно расшифрован!")
                case 0:
                    save_settings(settings)
                    return
                case _:
                    print("Указан неверный режим...\n")
                    continue
        except ValueError:
            print("Ошибка ввода...\n")
            continue
        except PermissionError:
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(e)
            continue


def main():
    """
    Точка входа в программу. Основная функция
    """
    print("Лабораторная работа №3. Построение гибридной криптосистемы..")
    settings_path = get_config_path()
    settings = load_settings(settings_path)
    while True:
        print("Выберете режим:\n[1] - Генерация ключей\n[2] - Шифрование\n[3] - Расшифровка\n[0] - Выход")
        try:
            choice = int(input())
            match choice:
                case 1:
                    generating(settings)
                case 2:
                    encrypting(settings)
                case 3:
                    decrypting(settings)
                case 0:
                    exit(0)
                case _:
                    print("Указан неверный режим...\n")
                    continue
        except ValueError:
            print("Ошибка ввода...\n")
        except PermissionError:
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(e)
            continue
 

if __name__ == "__main__":
    main()

from load_and_save import write_asymmetric_key, write_symmetric_key, write_text, read_asymmetric_key, read_symmetric_key,  read_text
from symmetric import get_symmetric_key, encrypt_text, decrypt_text
from asymmetric import encrypt_symmetric_key, decrypt_symmetric_key, get_asymmetric_key

def gen_logic(settings:dict) -> tuple:
    """консольный интерфейс"""
    print("Мастер генерации ключей")
    print("Ключ для 3DES алгоритма будет зашифрован с помощью RSA-OAEP")
    print("Возможная длинна ключа шифрования(в битах): 64, 128, 192")
    key_length = int(input("Выберите длинну ключа: "))
    while(key_length != 64 and key_length != 128 and key_length != 192):
        key_length = int(input("Выберите значения из списка!\n Ваш выбор: "))
    symmetric_key = get_symmetric_key(key_length // 8)
    private_key, public_key = get_asymmetric_key()
    encrypted_key = encrypt_symmetric_key(symmetric_key, public_key)
    print("Ключи успешно сгенерированы")
    print("Хотите использовать стандартные параметры сериализации ключей(Да\Нет)?")
    action = str(input("Да\Нет\n")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        print("Хотите использовать стандартные параметры сериализации ключей(Да\Нет)?")
        action = str(input()).lower()
    match action:
        case "нет":
            symmetric_key_path = str(input("Введите путь(имя) файла для сохранения 3DES ключа: "))
            write_symmetric_key(encrypted_key, symmetric_key_path)
            public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа: "))
            private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа: "))
            write_asymmetric_key(public_key, private_key, public_key_path, private_key_path)
            print("Ключи успешно сохранены")
            return symmetric_key, public_key, private_key
        case _:
            write_symmetric_key(encrypted_key, settings["symmetric_key_path"])
            write_asymmetric_key(public_key, private_key, settings["public_key_path"], settings["private_key_path"])
            print("Ключи успешно сохранены")
            return symmetric_key, public_key, private_key

def enc_logic(settings: dict):
    """консольный интерфейс"""
    print("Мастер шифровки текста")
    action = str(input("Желаете сгенерировать ключи шифрования?(Да\Нет): ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Желаете сгенерировать ключи шифрования?(Да\Нет): ")).lower()
    match action:
        case "нет":
            action = str(input("Ключи записаны в стандартные директории?(Да\Нет): ")).lower()
            while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
                action = str(input("Ключи записаны в стандартные директории?(Да\Нет): ")).lower()
            match action:
                case "нет":
                    symmetric_key_path = str(input("Введите путь(имя) файла 3DES ключа: "))
                    symmetric_key = read_symmetric_key(symmetric_key_path)
                    public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа: "))
                    private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа: "))
                    public_key, private_key = read_asymmetric_key(public_key_path, private_key_path)
                    symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
                    print("Ключи успешно загружены")
                case _:
                    symmetric_key = read_symmetric_key(settings["symmetric_key_path"])
                    public_key, private_key = read_asymmetric_key(settings["public_key_path"], settings["private_key_path"])
                    symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
                    print("Ключи успешно загружены")
        case _:
            symmetric_key, public_key, private_key = gen_logic()
    action = str(input("Текст записаны в стандартные директории?(Да\Нет): ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории?(Да\Нет): ")).lower()
    match action:
        case "нет":
            initial_file_path = str(input("Введите путь(имя) к тексту: "))
            text = read_text(initial_file_path)
        case _:
            text = read_text(settings["initial_file_path"])
    enc_text = encrypt_text(text, symmetric_key)
    print("Текст успешно зашифрован")
    action = str(input("Записать хашифрованный текст в стандартные директории?(Да\Нет): ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Записать хашифрованный текст в стандартные директории?: ")).lower()
    match action:
        case "нет":
            enc_path = str(input("Введите путь(имя) файла для сохранения зашифрованного сообщения: "))
            write_text(enc_text, enc_path)
        case _:
            write_text(enc_text, settings["encrypted_file_path"])
    return enc_text, symmetric_key
    

def dec_logic(settings: dict):
    """консольный интерфейс"""
    print("Мастер дешифровки текста")
    action = str(input("Ключи записаны в стандартные директории(Да\Нет)?: ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории(Да\Нет)?: ")).lower()
    match action:
        case "нет":
            symmetric_key_path = str(input("Введите путь(имя) файла 3DES ключа: "))
            symmetric_key = read_symmetric_key(symmetric_key_path)
            public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа: "))
            private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа: "))
            public_key, private_key = read_asymmetric_key(public_key_path, private_key_path)
            symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
            print("Ключи успешно загружены")
        case _:
            symmetric_key = read_symmetric_key(settings["symmetric_key_path"])
            public_key, private_key = read_asymmetric_key(settings["public_key_path"], settings["private_key_path"])
            symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
            print("Ключи успешно загружены")
    action = str(input("Текст записаны в стандартные директории?(Да\Нет): ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории?(Да\Нет): ")).lower()
    match action:
        case "нет":
            enc_path = str(input("Введите путь(имя) к тексту: "))
            text = read_text(enc_path)
        case _:
            text = read_text(settings["encrypted_file_path"])
    text = decrypt_text(text, symmetric_key)
    print("Текст успешно расшифрован")
    action = str(input("Записать расшифрованный текст в стандартные директории?(Да\Нет): ")).lower()
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Записать расшифрованный текст в стандартные директории?: ")).lower()
    match action:
        case "нет":
            enc_path = str(input("Введите путь(имя) файла для сохранения зашифрованного сообщения: "))
            write_text(text, enc_path)
        case _:
            write_text(text, settings["decrypted_file_path"])
    return text, symmetric_key
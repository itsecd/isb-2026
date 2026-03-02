import argparse
import sys




def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser()

    p.add_argument("-e",
                   "--encrypted_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\encrypted_text_task_2.txt",
                   help="Путь к зашифрованному тексту")

    p.add_argument("-kp",
                   "--key_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\key_task_2.txt",
                   help="Путь для сохранения значения ключа")

    p.add_argument("-d",
                   "--decrypted_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\decrypted_text_task_2.txt",
                   help="Путь для сохранения дешифрованного текста")

    return p.parse_args()



def main():
    args = parse_args()

    try:
        with open(args.encrypted_text_path, "r") as f:
            encrypted_text = f.read()
    except FileNotFoundError:
        print(f"File path {args.encrypted_text_path} was not found")
        sys.exit(1)






if __name__ == "__main__":
    main()
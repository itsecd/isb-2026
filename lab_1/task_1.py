import sys

def main():
    original_text_path = ("C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                          "isb-2026\\lab_1\\original_text_task_1.txt")
    key_path = ("C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                "isb-2026\\lab_1\\key_task_1.txt")
    encrypted_text_path = ("C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\modified_text_task_1.txt")

    decrypted_text_path = ("C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\decrypted_text_task_1.txt")

    try:
        with open(original_text_path, "r") as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"File path {original_text_path} was not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
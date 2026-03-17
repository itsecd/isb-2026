import sys
from config import RUSSIAN_FREQ
import transposition
import frequency
import file_utils


def task1_encrypt():
    """Задание 1: шифрование текста """
    print("Шифрование текста постолбцовой транспоизицей")

    original_text = file_utils.read_text_from_file('task1_original.txt')

    if original_text is None:
        print("\nСоздайте файл task1_original.txt с исходным текстом и запустите программу снова.")
        return

    print(f"\nИсходный текст из файла:")
    print(original_text)

    while True:
        keyword = input("\nВведите ключевое слово для шифрования: ").upper().strip()
        if keyword:
            if all(c.isalpha() for c in keyword):
                break
            else:
                print("Ключ должен содержать только буквы!")
        else:
            print("Ключ не может быть пустым!")

    print(f"\nКлюч: '{keyword}'")

    encrypted = transposition.encrypt(original_text, keyword)

    print("\nЗашифрованный текст:")
    print(encrypted)

    print("\nСохранение файлов:")
    file_utils.save_text(encrypted, 'task1_encrypted.txt')
    file_utils.save_key(keyword, 'task1_key.txt')

    decrypted = transposition.decrypt(encrypted, keyword)

    print("\nДешифрованный текст:")
    print(decrypted)

    if decrypted == original_text:
        print("\nТекст успешно дешифруется обратно")
    else:
        print("\nОшибка: дешифрованный текст не совпадает с исходным")


def task2_decrypt():
    """Задание 2: частотный анализ для дешифровки """
    print("\nЧастотный анализ текста из задания 2")

    encrypted_text = file_utils.read_text_from_file('cod6.txt')

    if encrypted_text is None:
        print("\nСоздайте файл cod6.txt с текстом из варианта 6 и запустите программу снова.")
        return

    frequencies = frequency.analyze(encrypted_text)
    frequency.print_table(frequencies)

    print("\nСохрание файлов:")
    file_utils.save_frequency_analysis(frequencies, 'task2_freq_analysis.txt')

def main():
    task1_encrypt()
    task2_decrypt()

if __name__ == "__main__":
    main()
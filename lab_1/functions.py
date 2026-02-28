# -*- coding: utf-8 -*-
"""Functions"""

from constants import RU_ALPHABET


def vigenere_encrypt(text, key):
    """Vigenere cipher"""


    encrypted_text = []
    key_length = len(key)
    text = text.upper()
    
    for i in range(len(text)):
        current_char = text[i]

        char_index = RU_ALPHABET.find(current_char)
         
        if char_index != -1:
            key_char = key[i % key_length]
            key_index = RU_ALPHABET.find(key_char.upper())

            new_index = (char_index + key_index) % 33
            encrypted_text.append(RU_ALPHABET[new_index])
        else:
            encrypted_text.append(current_char)

    return ''.join(encrypted_text)


def create_key():
    """Creating encryption key"""
    return "ПЕПС"


def write_to_files(original_text, encrypted_text, key):
    """Function for writing to files"""

    with open('encrypted_text.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    
    with open('original_text.txt', 'w', encoding='utf-8') as file:
        file.write(original_text)
 
    with open('encryption_key.txt', 'w', encoding='utf-8') as file:
        file.write(f"Ключ шифрования: {key}\n")
        file.write(f"Длина ключа: {len(key)}\n")


def main():
    plain_text = """Власти готовят финальный удар по Telegram
Российские власти определились со сроками полной блокировки мессенджера Telegram. По данным источников, знакомых с обсуждениями в профильных ведомствах, отключение планируют провести в начале апреля. Два источника, близких к Кремлю, называют это окончательным решением. Главная причина - участившиеся случаи вербовки граждан и несовершеннолетних для противоправной деятельности.
В отношении основателя Telegram Павла Дурова расследуется уголовное дело по статье о содействии террористической деятельности. Ч. 1.1 ст. 205.1 УК России предусматривает от восьми лет до пожизненного лишения свободы. Сам Дуров связал это с попыткой подавить право на частную жизнь и свободу слова.
Блокировке предшествовали постепенные ограничения работы мессенджера. С 10 февраля власти начали замедлять Telegram, а ранее ограничили голосовые звонки, объясняя это защитой граждан от мошенничества и вовлечения в противоправную деятельность."""
    
    plain_text = ' '.join(plain_text.split())
    
    key = create_key()
    encrypted_text = vigenere_encrypt(plain_text, key)
    write_to_files(plain_text, encrypted_text, key)

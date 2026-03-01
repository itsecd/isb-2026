# -*- coding: utf-8 -*-
"""Functions"""

from constants import RU_ALPHABET


def vigenere_encrypt(text: str, key: str) -> str:
    """Vigenere cipher"""


    encrypted_text: list[str] = []
    key_length: int = len(key)
    text = text.upper()
    
    for i in range(len(text)):
        current_char: str = text[i]
        char_index: int = RU_ALPHABET.find(current_char)
         
        if char_index != -1:
            key_char: str = key[i % key_length]
            key_index: int = RU_ALPHABET.find(key_char.upper())

            new_index: int = (char_index + key_index) % 33
            encrypted_text.append(RU_ALPHABET[new_index])
        else:
            encrypted_text.append(current_char)

    return ''.join(encrypted_text)


def create_key() -> str:
    """Creating encryption key"""
    return "ПЕПС"


def write_to_files(
        original_text: str,
        encrypted_text: str,
        key: str) -> None:
    """Function for writing to files"""

    with open('encrypted_text.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    
    with open('original_text.txt', 'w', encoding='utf-8') as file:
        file.write(original_text)
 
    with open('encryption_key.txt', 'w', encoding='utf-8') as file:
        file.write(f"Ключ шифрования: {key}\n")
        file.write(f"Длина ключа: {len(key)}\n")


def main() -> None:
    plain_text: str = """Власти готовят финальный удар по Telegram
Российские власти определились со сроками полной блокировки мессенджера Telegram. По данным источников, знакомых с обсуждениями в профильных ведомствах, отключение планируют провести в начале апреля. Два источника, близких к Кремлю, называют это окончательным решением. Главная причина - участившиеся случаи вербовки граждан и несовершеннолетних для противоправной деятельности.
В отношении основателя Telegram Павла Дурова расследуется уголовное дело по статье о содействии террористической деятельности. Ч. 1.1 ст. 205.1 УК России предусматривает от восьми лет до пожизненного лишения свободы. Сам Дуров связал это с попыткой подавить право на частную жизнь и свободу слова.
Блокировке предшествовали постепенные ограничения работы мессенджера. С 10 февраля власти начали замедлять Telegram, а ранее ограничили голосовые звонки, объясняя это защитой граждан от мошенничества и вовлечения в противоправную деятельность."""
    
    plain_text = ' '.join(plain_text.split())
    
    key: str = create_key()
    encrypted_text: str = vigenere_encrypt(plain_text, key)
    write_to_files(plain_text, encrypted_text, key)

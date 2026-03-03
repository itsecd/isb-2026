from typing import Dict, Optional

from constants import RUSSIAN_ALPHABET, ALPHABET_LENGTH


def caesar_encrypt(text: str, shift: int) -> str:
    """
    Шифрует текст шифром Цезаря с заданным сдвигом.
    
    Args:
        text: Исходный текст для шифрования
        shift: Величина сдвига (положительное число)
    
    Returns:
        str: Зашифрованный текст
    
    Raises:
        ValueError: Если текст содержит символы, отсутствующие в алфавите
    """
    result = []
    
    for char in text:
        upper_char = char.upper()
        
        if upper_char in RUSSIAN_ALPHABET:
            idx = RUSSIAN_ALPHABET.index(upper_char)
            new_idx = (idx + shift) % ALPHABET_LENGTH
            encrypted_char = RUSSIAN_ALPHABET[new_idx]
            
            if char.islower():
                encrypted_char = encrypted_char.lower()
            
            result.append(encrypted_char)
        
        else:
            #Символы не из алфавита не меняем
            result.append(char)
    
    return "".join(result)


def caesar_decrypt(encrypted_text: str, shift: int) -> str:
    """
    Дешифрует текст, зашифрованный шифром Цезаря.
    
    Args:
        encrypted_text: Зашифрованный текст
        shift: Величина сдвига, использованная при шифровании
    
    Returns:
        str: Расшифрованный текст
    """
    return caesar_encrypt(encrypted_text, -shift)


def shift_to_key(shift: int) -> Dict[str, str]:
    """
    Преобразует сдвиг в формат ключа подстановки.
    
    Args:
        shift: Величина сдвига
    
    Returns:
        Dict[str, str]: Ключ подстановки (словарь: исходная буква -> замена)
    """
    key = {}
    for i, char in enumerate(RUSSIAN_ALPHABET):
        new_idx = (i + shift) % ALPHABET_LENGTH
        key[char] = RUSSIAN_ALPHABET[new_idx]
    return key


def save_shift(shift: int, filename: str) -> None:
    """
    Сохраняет сдвиг в файл.
    
    Args:
        shift: Величина сдвига
        filename: Имя файла для сохранения
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"shift:{shift}\n")
        f.write("Подстановка (исходная -> замена):\n")
        for i, char in enumerate(RUSSIAN_ALPHABET):
            new_idx = (i + shift) % ALPHABET_LENGTH
            f.write(f"{char}:{RUSSIAN_ALPHABET[new_idx]}\n")
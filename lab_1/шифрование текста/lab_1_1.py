def vigenere_encrypt(text, key):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    clean_key = ''
    key = key.lower()
    for char in key:
        if char in alphabet:
            clean_key += char
    
    if not clean_key:
        return "Ошибка: ключ должен содержать буквы русского алфавита"
    
    result = ''
    key_index = 0
    
    for char in text:
        if char in alphabet:
            pos = 0
            while pos < len(alphabet) and alphabet[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos + key_pos) % 33
            result += alphabet[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
            
        elif char in alphabet_upper:
            pos = 0
            while pos < len(alphabet_upper) and alphabet_upper[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos + key_pos) % 33
            result += alphabet_upper[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
        else:
            result += char
    
    return result


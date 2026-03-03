def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)

def get_pos(char):
    lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    if char in lower:
        return lower.index(char)
    elif char in upper:
        return upper.index(char)
    else:
        return -1

def get_char_by_pos(pos, is_upper):
    lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    if is_upper:
        return upper[pos % 33]
    else:
        return lower[pos % 33]

def encrypt(text, key):
    encrypted_text = []
    key = generate_key(text, key)
    
    for i in range(len(text)):
        char = text[i]
        pos = get_pos(char)
        
        if pos != -1:
            is_upper = char.isupper()
            key_pos = get_pos(key[i])
            encrypted_pos = (pos + key_pos) % 33
            encrypted_char = get_char_by_pos(encrypted_pos, is_upper)
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def decrypt(encrypted_text, key):
    decrypted_text = []
    key = generate_key(encrypted_text, key)
    
    for i in range(len(encrypted_text)):
        char = encrypted_text[i]
        pos = get_pos(char)
        
        if pos != -1: 
            is_upper = char.isupper()
            key_pos = get_pos(key[i])

            decrypted_pos = (pos - key_pos + 33) % 33
            decrypted_char = get_char_by_pos(decrypted_pos, is_upper)
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

def main():
    original_text = """
Раннее утро в небольшом городке всегда особенное — воздух ещё свеж и прохладен, 
а первые лучи солнца мягко золотят крыши домов. Улицы почти пусты: лишь изредка мелькнёт фигура
 спешащего на работу человека или пробежит заигравшийся пёс. В парках слышно пение ранних птиц — 
 звонкие трели соловьёв переплетаются с размеренным стуком дятла.

Возле пекарни уже чувствуется аппетитный аромат свежевыпеченного хлеба, а у цветочного киоска 
раскладывают первые букеты: нежные тюльпаны, гордые нарциссы и скромные подснежники. Где‑то вдалеке 
гудит мусоровоз, но этот звук не нарушает общей умиротворяющей атмосферы — он лишь подчёркивает начало 
нового дня, полного возможностей и маленьких радостей. Горожане постепенно просыпаются, и жизнь набирает обороты."""

    key = "КРИПТОГРАФИЯ"
    
    print("Исходный текст:")
    print(original_text)
    print(f"\nДлина текста: {len(original_text)} символов")
    print(f"Ключевое слово: {key}")
    print(f"Длина ключа: {len(key)} символов")
    
    encrypted = encrypt(original_text, key)

    print("ЗАШИФРОВАННЫЙ ТЕКСТ:")
    print(encrypted)
    
    decrypted = decrypt(encrypted, key)
    print("ДЕШИФРОВАННЫЙ ТЕКСТ:")
    print(decrypted)
    
    print("ПРОВЕРКА:")
    if original_text == decrypted:
        print("Дешифрованный текст полностью совпадает с исходным.")
    else:
        print("Дешифрованный текст отличается от исходного.")
            
    print("ДЕМОНСТРАЦИЯ РАБОТЫ:")
    test_text = "Привет, мир!"
    test_key = "Ключ"
    print(f"Тестовый текст: '{test_text}'")
    print(f"Ключ: '{test_key}'")
    
    test_encrypted = encrypt(test_text, test_key)
    test_decrypted = decrypt(test_encrypted, test_key)
    
    print(f"Зашифровано: '{test_encrypted}'")
    print(f"Расшифровано: '{test_decrypted}'")
    
if __name__ == "__main__":
    main()
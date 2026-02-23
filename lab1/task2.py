import collections

def load_key_from_file(filename):
    """Загружает ключ дешифровки из файла"""
    key = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '->' not in line:
                    continue
                parts = [p.strip() for p in line.split('->')]
                if len(parts) != 2:
                    continue
                cipher, plain = parts
                if cipher == 'M':
                    key['M'] = ' '
                else:
                    key[cipher] = plain
        return key
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении ключа: {e}")
        return {}

def count_freq(text):
    """Считает частоту символов"""
    counter = collections.Counter(text)
    total = sum(counter.values())
    if total == 0:
        return {}
    freq = {char: count / total for char, count in counter.most_common()}
    return freq

def decrypt(text, key):
    """Расшифровывает текст, заменяя символы по ключу"""
    result = []
    for char in cipher_text:
        if char in key:
            result.append(key[char])
        else:
            result.append(char)
    text = ''.join(result)
    text = text.replace('. ', '.\n').replace('! ', '!\n').replace('? ', '?\n')
    return text.strip()

def main():
    try:
        with open('task2_cod1.txt', 'r', encoding='utf-8') as f:
            cipher_text = f.read()        
        key = load_key_from_file('task2_key.txt')
        if not key:
            print("Ключ пустой — дешифровка невозможна")
            return
        freq = count_freq(cipher_text)
        with open('task2_freq.txt', 'w', encoding='utf-8') as f:
            f.write("Символ | Частота\n")
            f.write("----------------\n")
            for char, f_val in freq.items():
                display_char = repr(char) if char.isspace() else char
                f.write(f"{display_char:6} | {f_val:.5f}\n")
        decrypted_text = decrypt(cipher_text, key)

        with open('task2_decryption.txt', 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
        print("Дешифровка успешно выполнена")
    except Exception as e:
        print(f"Ошибка: {e}")
        
if __name__ == "__main__":
    main()

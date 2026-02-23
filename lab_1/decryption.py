
def decrypt_text(text : str) -> str:
    crypto_key = {
        'c': ' ', 'А': 'О', 'Х': 'И', '8': 'Е', 'М': 'Т', 
        'r': 'Н', 'Л': 'С', 'О': 'А', '2': 'К', 'b': 'Я', 
        'К': 'Р', 'Е': 'М', 'Д': 'Л', 'Б': 'П', 'Р': 'В', 
        '7': 'Д', '4': 'Ь', 't': 'У', '<': 'Ч', '1': 'Й', 
        'Ф': 'З', 'У': 'Ж', '5': 'Э', '>': 'Г', 'Ч': 'Ц', 
        '?': 'Ы', 'И': 'Ф', 'П': 'Б', 'a': 'Ю', 'Й': 'Х', 
        'Ь': 'Щ', 'Ы': 'Ш'
    }

    plaintext = "".join(crypto_key.get(char,char) for char in text)

    return plaintext

def get_freq(text:str) -> str:
    len_t = len(text)
    char_freq = {i: text.count(i)/len_t for i in text}
    freq_char = {key: value for key, value in sorted(char_freq.items(), key= lambda item: item[1], reverse=True)}
    return str(freq_char)

def write_file(path : str,text : str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def open_file(path : str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    print(f"Зашифрованный текст:\n{open_file("cod18.txt")}\n")
    print(f"Расшифрованный текст:\n{decrypt_text("cod18.txt")}")


if __name__ == "__main__":
    main()

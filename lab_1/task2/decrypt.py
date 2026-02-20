import work_file2


def get_frequency(text: str) -> dict:
    """
    Вычисляет относительную частоту появления каждого символа в тексте.
    """
    fre_dict = {}
    size = len(text)
    for i in text:
        fre_dict[i] = fre_dict.get(i, 0) + 1
    for i in fre_dict:
        fre_dict[i] = fre_dict[i] / size
    return dict(sorted(fre_dict.items(), key=lambda item: item[1], reverse=True))

def get_key(dict_fi: dict, dict_se:dict) -> dict:
    """
    Формирует ключ замены на основе двух частотных словарей.
    """
    new_dict = {}

    for key1, key2 in zip(dict_fi.keys(), dict_se.keys()):
        new_dict[key1] = key2
    return new_dict


def repalce_text(text: str, key: dict) -> str:
    """
    Выполняет замену символов в тексте согласно заданному ключу.
    """
    decrypted_text = ""
    for i in text:
        decrypted_x = key.get(i)
        if decrypted_x is None:
            decrypted_x = i
        decrypted_text += decrypted_x
    return decrypted_text

def main():
    """Основная функция"""

    encrypted_text = work_file2.read_file_txt("cod18")

    freq_encrypted = get_frequency(encrypted_text)

    work_file2.write_file("freq_encrypted",freq_encrypted)
    
    freq_sample = work_file2.read_file("sample_frequency")

    key_fi =  get_key(freq_encrypted, freq_sample)

    work_file2.write_file("key_fi",key_fi)

    decrypted_text = repalce_text(encrypted_text, key_fi) 

    work_file2.write_file_txt("decrypted_text", decrypted_text)


if __name__ == "__main__":
    main()
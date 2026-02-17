alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'

def load_key_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    words = content.split()
    return words[-1].strip() if words else ''

def char_to_index(char):
    return alphabet.index(char)

def index_to_char(index):
    return alphabet[index % len(alphabet)]

def encryption(text, keyword):
    text = text.upper()
    keyword = keyword.upper()
    key_indices = [char_to_index(k) for k in keyword if k in alphabet]

    result = []
    key_pos = 0

    for char in text:
        if char in alphabet:
            shift = key_indices[key_pos % len(key_indices)]
            enc_idx = (char_to_index(char) + shift) % len(alphabet)
            result.append(index_to_char(enc_idx))
            key_pos += 1
        else:
            result.append(char)

    return ''.join(result)

keyword = load_key_from_file('task1_key.txt')

text = """Масленица — это древний славянский праздник проводов зимы, который длится целую неделю перед Великим постом. Главное угощение на Масленицу — блины, они символизируют солнце и тепло. Каждый день недели имеет своё название. В конце праздничной недели, сжигают чучело зимы, чтобы весна скорее вступила в свои права. Люди просят друг у друга прощения и готовятся к самому строгому посту. Все радуются блинам ходят в гости и веселятся перед долгим воздержанием. Традиция печь блины пришла из глубины веков и сохранилась до наших дней."""

encrypted_text = encryption(text, keyword)

with open('task1_original.txt', 'w', encoding='utf-8') as f:
    f.write(text)

with open('task1_encryption.txt', 'w', encoding='utf-8') as f:
    f.write(encrypted_text)

print(f"\nШифрование успешно завершено")
def mapper(text: str, map: dict) -> str:
    """Заменяет символы в исходном тексте на основе словаря map"""
    res = ""
    for c in text:
        if c in map.keys():
            res += map[c]
        else:
            res += c
    return res


def main() -> None:
    A = " ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"

    with open("cod4.txt", encoding="utf-8", mode="r") as f:
        data = f.read()
    
    char_data = dict.fromkeys(set(data), 0)
    for c in data:
        char_data[c] += 1

    for k, v in char_data.items(): 
        char_data[k] = (v, v / len(data))
    # Непонятный код для сортировки по символов исходного текста по частоте (и лекс. порядку в случае равенства)
    results = sorted(list(char_data.items()), key=lambda x: (x[1][0], x[0]), reverse=True) 

    map = {
        "г": " ", "О": "И", "Д": "О", # Начало
        "<": "С", "@": "Л", # Догадка с "или"
        "R": "П", "J": "Н", "N": "Ф", "3": "Д", "Y": "Р", "1": "М", "Р": "А", "i": "Ц", # Слово "ИНФОРМАЦИЯ"
        "Q": "Б", "у": "Е", "Ж": "З", "9": "Т", "F": "Ь", "И": "Ю", "U": "Я", # безопасность
        "ю": "Щ", "Й": "У", "Т": "Ж", "Я": "В", "Z": "К", "К": "Ы", "Ё": "Ч", "%": "Х", # и т.д.
        "7": "Г",
        "=": "Ъ", "s": "Ш", "G": "Э", "\n": "\n"
    }

    for k, v in results:
        print(f'"{k.strip()}": {v[1]:.5f} -> "{map[k].strip()}"')

    print(f"{len(map.keys())}/{len(A)}")

    data_map = mapper(data, map=map)

    n = 1
    for s in data_map.split(): # Вывод по 4 слова для удобства.
        print(s, end=" ")
        if n % 4 == 0:
            print()
        n += 1
    
    with open("cod4_decrypted.txt", encoding="utf-8", mode="w") as f:
        f.write(data_map)
    

if __name__ == "__main__":
    main()
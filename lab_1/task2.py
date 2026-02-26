from cod4_key import KEY
from constants import TASK2_INPUT, TASK2_OUTPUT

def mapper(text: str, map: dict) -> str:
    """Заменяет символы в исходном тексте на основе словаря map"""
    res = ""
    for c in text:
        if c in map.keys():
            res += map[c]
        else:
            res += c
    return res

def frequencies(text: str) -> list[(str, float)]:
    char_data = dict.fromkeys(set(text), 0)
    for c in text:
        char_data[c] += 1
    for k, v in char_data.items(): 
        char_data[k] = v / len(text)

    # Сортировка символов текста по частоте (и лекс. порядку в случае равенства)
    res = list(sorted(char_data.items(), key=lambda x: (x[1], x[0]), reverse=True))
    return res


def main() -> None:
    with open(TASK2_INPUT, encoding="utf-8", mode="r") as f:
        data = f.read()
    
    char_frequencies = frequencies(data)

    for char, value in char_frequencies:
        print(f'"{char.strip()}": {value:.5f}')

    data_map = mapper(data, map=KEY)
    n = 1
    for s in data_map.split(): # Вывод по 4 слова для удобства.
        print(s, end=" ")
        if n % 4 == 0:
            print()
        n += 1
    
    with open(TASK2_OUTPUT, encoding="utf-8", mode="w") as f:
        f.write(data_map)
    

if __name__ == "__main__":
    main()
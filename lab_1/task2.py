def mapper(text: str) -> str:
    map = { "О": " "}
    res = ""
    for c in text:
        if c in map.keys():
            res += map[c]
        else:
            res += c
    return res


def main() -> None:
    with open("lab_1/cod4.txt", encoding="utf-8", mode="r") as f:
        data = f.read()
    
    char_data = dict.fromkeys(set(data), 0)
    for c in data:
        char_data[c] += 1
    print(*sorted(list(char_data.items()),key=lambda x: x[1], reverse=True)[0:10], "...")

    data_map = mapper(data)
    print(data_map)
    

if __name__ == "__main__":
    main()
import re

def staticstic(text: str) -> dict:
    word_set = set(text)
    dictionary = {i:0 for i in word_set}
    for word in text:
            dictionary[word] += 1
    for i,j in dictionary.items():
         dictionary[i] = j/len(text)
    sorted_dictonary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    return sorted_dictonary

def decode(text:str, key:dict) -> str: 
    for i, j in key.items():
        text = text.replace(i, j)
    return text    

def str_to_dict(str: str) -> dict:
    str = str.split("\n")
    dict_str={}
    for k in str:
        buf = re.split(r"[\n\t,;]", k)
        dict_str[buf[0]]=buf[1]
    return dict_str

def main() -> None:
    with open("cod21.txt", encoding="utf-8") as file:
            text = file.read()
    with open("stats.txt", "w", encoding="utf-8") as f:
            for i,j in staticstic(text).items():
                  f.write(i + "\t" + str(j) + "\n")
    with open("key.txt", encoding="utf-8") as file:
            key = file.read()
    key = str_to_dict(key)
    answer = decode(text, key)
    with open("decode.txt", "w", encoding="utf-8") as f:
         f.write(answer)
    print("program end")


if __name__ == "__main__":
     main()
def staticstic(text: str) -> dict:
    word_set = set(text)
    dictionary = {i:0 for i in word_set}
    for word in text:
         dictionary[word] += 1
    for i,j in dictionary.items():
         dictionary[i] = j/len(text)
    sorted_dictonary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    return sorted_dictonary

        

def main() -> None:
    with open("orig_2.txt", encoding="utf-8") as file:
            text = file.read()
    with open("statistic.txt", "w", encoding="utf-8") as f:
            for i,j in staticstic(text).items():
                  f.write(i + " " + str(j) + "\n")
    print("OK")

if __name__ == "__main__":
     main()
        
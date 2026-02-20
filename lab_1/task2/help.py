def fileopen(filename: str) -> str:
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise e
    
def mapper(text: str):
    result = {}
    for i in text:
        if i in result:
            result[i]+=1/1100
        else:
            result[i]=1/1100
            
    result = {k: round(v, 5) for k, v in result.items()}
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return result


def main():
    text = fileopen("lab_1/task2/cod3.txt")
    map = mapper(text)
    print(len(map))
    print(map)

if __name__ == "__main__":
    main()
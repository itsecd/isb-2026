import random
from config import FILE_PATH

def generator()-> str:
    res = ""
    for i in range(129):
        rand = random.randint(0,1)
        res += str(rand)
    
    return res

def to_file(text:str, path:str)-> None:
    with open(path, "w", encoding= "utf-8") as f:
        f.write(text)
    
def main():
    res = generator()
    to_file(res, FILE_PATH)

if __name__ == "__main__":
    main()
        
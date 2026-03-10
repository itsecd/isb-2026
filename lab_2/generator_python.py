import random

def write_text(filename: str, text: str) -> str:   
    try:
        with open(filename,"w", encoding="utf-8") as f:  
            f.write(text)
    except FileNotFoundError:
        raise 

def main() ->None:
    seq=""
    
    for i in range(128):
        seq+=str(random.randint(0,1))
    
    write_text("seq_python.txt", seq)


if __name__ == "__main__":
    main()
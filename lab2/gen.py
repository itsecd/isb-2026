from random import randint

def Generator() -> None:
    '''ГСПЧ'''
    with open("out_py.txt", mode='w', encoding='utf-8') as f:
        for i in range (0,128):
            f.write(f"{randint(0,1)}")
    

if __name__ == "__main__":
    Generator()
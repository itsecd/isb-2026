import argparse

alphabet_upper = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

def encode(text,key):
    table=[]
    for i in range(len(alphabet_upper)):
        row=alphabet_upper[i:]+alphabet_upper[:i]
        table.append(row)

    encode_text=""
    key_counter = 0
    for i in range(len(text)):
        char=text[i]
        char_upper=char.upper()

        if char_upper in alphabet_upper:
            key_char=key[key_counter%len(key)]
            key_index=alphabet_upper.index(key_char.upper())

            if key_index==-1:
                encode_text+=char
                continue
            
            char_index=alphabet_upper.index(char_upper)
            encode_char=table[char_index][key_index]
            encode_text+=encode_char
            
            key_counter+=1
    return encode_text

def take_key(filenamekey):
    with open(filenamekey,"r",encoding="utf-8") as file:
        key=file.read().strip()
        return key
    
def take_text(filenametext):
    with open(filenametext,"r",encoding="utf-8") as file:
        text=file.read()
        return text
    
def write_result(encode_text,filenameoutput):
    with open(filenameoutput,"w",encoding="utf-8") as file:
        file.write(encode_text)

def parsing():
    parser=argparse.ArgumentParser()
    parser.add_argument("filenametext",type=str,help="Введите названия файла с исходным текстом")
    parser.add_argument("filenamekey",type=str,help="Введите название файла с ключом")
    parser.add_argument("filenametextoutput",type=str,help="Введите названия файла с результатом")
    args=parser.parse_args()
    return args.filenametext,args.filenamekey,args.filenametextoutput

def main():
    filenametext,filenamekey,filenameoutput=parsing()
    key=take_key(filenamekey)
    text=take_text(filenametext)
    encode_text=encode(text,key)
    write_result(encode_text,filenameoutput)

if __name__=="__main__":
    main() 
    """
    py main.py unencoded_text.txt key.txt result.txt
    """
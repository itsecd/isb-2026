cipher_text = """PE!WFxZ!CFU!9Fn!CAS$nFSZtI!IOZ>hIKn!9AAW$ZU9tnWZEAnI!AInFCLnx
ZFYQVAxIZA9FEnIhEZEZ=!WBEIZKCAChx
9AEZV9BWnZVCFKE!9PCnFSZU9=ZU9hIOAxIZU!9B!CVVxZEhEZ3CLhxZtn9MxZ9MVCAWn-ZU9hO9PCnIhSZEZOCFnCPEn-ZIB9ZOCUWFnEn-ZPE!WF
tn9MxZOC8EnEn-FSZ9nZPE!WF9PZAI9MG9=EV9ZEFU9h-O9PCnZCAnEPE!WFA9IZU!9B!CVVA9IZ9MIFUItIAEIZK9n9!9IZV9JInZ9MAC!WJ
EPCn-ZEZW=ChSn-ZPE!WFxZEOZFEFnIVx
nCKJIZPCJA9ZAIZ9nK!xPCn-ZU9=9O!EnIh-AxIZUEFVCZEZFFxhKEZAIZOCB!WJCnZ3CLhxZEOZAIAC=QJAxGZEFn9tAEK9PZEZ!IBWhS!A9Z9MA9PhSnZ9UI!CRE9AAW$ZFEFnIVWZEZU!Eh9JIAES
IFhEZPxZU9=9O!IPCInIZtn9ZPCdZK9VU-$nI!ZEhEZV9MEhA9IZWFn!9LFnP9ZOC!CJIA9ZPE!WF9VZAIVI=hIAA9Z9M!CnEnIFZKZFUIREChEFnWZU9ZEA39!VCRE9AA9LZMIO9UCFA9FnEZEhEZEFU9h
-
OWLnIZCAnEPE!WFAW$ZU!9B!CVVWZ=hSZFKCAE!9PCAESZEZ9tEFnKE
ZFEFnIVx"""

key = {
    'n': 'т',
    '-': 'ь',
    'h': 'л',
    'E': 'и',
    'g': 'о',
    'O': 'з',
    'Z': ' ',
    'U': 'п',
    '=': 'д',
    '!': 'р',
    'I': 'е',
    'A': 'н',
    'x': 'ы',
    'F': 'с',
    'V': 'м',
    'W': 'у',
    'R': 'ц',
    'K': 'к',
    '$': 'ю',
    'C': 'а',
    'P': 'в',
    'S': 'я',
    'M': 'б',
    'B': 'г',
    't': 'ч',
    '8': 'щ',
    '>': 'э',
    'L': 'й',
    'Y': 'ъ',
    'Q': 'ё',
    '3': 'ф',
    'G': 'х',
    'J': 'ж',
    '9': 'о'  
}

def decrypt(text, key):
    result = []
    for line in text.split('\n'):
        decrypted_line = ''
        for char in line:
            if char in key:
                decrypted_line += key[char]
            else:
                decrypted_line += char  #как есть, если нет в ключе
        result.append(decrypted_line)
    return '\n'.join(result)

decrypted_text = decrypt(cipher_text, key)

with open('Task2_decrypted_text.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted_text)

with open('Text2_key.txt', 'w', encoding='utf-8') as f:
    f.write("ИСПОЛЬЗОВАННЫЙ КЛЮЧ:\n")
    f.write("=" * 30 + "\n")
    for k in sorted(key.keys()):
        f.write(f"'{k}' -> '{key[k]}'\n")

print("\nГотово!")
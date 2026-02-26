'''Шифр Виженера'''

def keyIsValidVig(key, alphabet):
    '''Проверяет формат ключа для алгоритма Виженера'''
    for symbol in key:
        if symbol not in alphabet:
            return False
    return True

def encryptMessageViginer(key, alphabet, message):
    '''Запускает функцию шифровки/расшифровки с параметром 'encrypt'

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо зашифровать 
    '''

    return translateMessage(key, alphabet, message, 'encrypt')

def decryptMessageViginer(key, alphabet, message):
    '''Запускает функцию шифровки/расшифровки с параметром 'decrypt'

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо расшифровать  
    '''

    return translateMessage(key, alphabet, message, 'decrypt')

def translateMessage(key, alphabet, message, mode):
    '''Функция шифровки/расшифровки сообщения алгоритмом Виженера

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо зашифровать/расшифровать
    mode: операция (зашифровать\расшифровать)
    '''

    translated = []
    
    
    mesDelSpace = message.replace('\n', '')
    keyIndex = 0
    key = key.upper()
    
    for symbol in mesDelSpace:
        num = alphabet.find(symbol.upper())
        if num!= -1:
            if mode == 'encrypt':
                num+=alphabet.find(key[keyIndex])
            
            elif mode == 'decrypt':
                num-=alphabet.find(key[keyIndex])

            num%=len(alphabet)

            if symbol.isupper():
                translated.append(alphabet[num])
            elif symbol.islower:
                translated.append(alphabet[num].lower())

            keyIndex += 1
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)
    return ''.join(translated)



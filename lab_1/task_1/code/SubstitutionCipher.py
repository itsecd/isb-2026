'''Шифр простой подстановки'''

def keyIsValidSub(key, alphabet) -> bool:
    '''Проверяет формат ключа для алгоритма простой подстановки'''
    keySet = set(key)
    print(len(keySet))
    return len(alphabet) == len(keySet)

def encryptMessageSubstitution(key, alphabet, message)->str:
    '''Запускает функцию шифровки/расшифровки с параметром 'encrypt'

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо зашифровать 
    '''
    return translateMessage(key, alphabet, message, 'encrypt')

def decryptMessageSubstitution(key, alphabet, message)->str:
    '''Запускает функцию шифровки/расшифровки с параметром 'decrypt'

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо расшифровать  
    '''
    return translateMessage(key, alphabet, message, 'decrypt')

def translateMessage(key, alphabet, message, mode)->str:
    '''Функция шифровки/расшифровки сообщения алгоритмом простой подстоновки

    key: ключ шифрования
    alphabet: набор символов на котором записано расшифрованное сообщение 
    message: сообщение которое надо зашифровать/расшифровать
    mode: операция (зашифровать\расшифровать)
    '''
    tranlated = []
    charsA = alphabet
    charsB = key.upper()
    if mode == 'decrypt':
        charsA, charsB = charsB, charsA

    for symbol in message:
        if symbol.upper() in charsA:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                tranlated.append(charsB[symIndex].upper())
            else:
                tranlated.append(charsB[symIndex].lower())
        else:
            tranlated.append(symbol)
    print(''.join(tranlated))
    return ''.join(tranlated)
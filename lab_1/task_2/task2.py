"""
Модуль для частотного анализа и дешифровки текста.
"""

ETAOIN = " ОЕАИНТСРВЛКМДПУЯЫЬГЗБЧЙХЖШЮЦЩЭФЪ"
LETTERS = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

def read_file(path: str) -> str:
    ''' Читает файл и возвращает строку.'''
    try:
        with open(path, "r", encoding='utf-8') as file:
            lines = file.read()
            return lines
        print(f"Файл {path} не найден")
        return None
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None


def saveStatistics(freqPairs:list, lenText:int):
    """
    Сохраняет статистику частотности букв в файл
    freqPairs: Список пар (частота, буквы)
    lenText: Длина текста для вычисления относительной частоты
    """
    with open('.\\lab_1\\task_2\\statistics.txt', 'w', encoding='utf-8') as f:
        for freq, letters in freqPairs:
            relative_freq = freq / lenText
            rounded_freq = round(relative_freq, 5)
            for letter in letters:
                f.write(f"{letter} {rounded_freq}\n")
    
    print("Файл statistics.txt сохранен")

def saveKey(key:dict):
    """
    Сохраняет ключ дешифровки в файл.
    key: Словарь с ключом дешифровки
    """
    with open(".\\lab_1\\task_2\\key.txt", 'w', encoding='utf-8') as f:
        for cipher_char, plain_char in key.items():
            f.write(f"{cipher_char} {plain_char}\n")
    
    print(f"Файл key.txt успешно сохранен")

def saveResult(result:str):
    """Сохраняет результат дешифровки в файл""" 
    with open('.\\lab_1\\task_2\\result.txt', "w", encoding='utf-8') as file:
        file.write(result)
    print(f"Файл result.txt успешно сохранен")

def getLetterCount(message:str)->tuple:
    """ Подсчитывает частоту каждой буквы в сообщении"""
    letterCount = {}
    lettersInText = ""
    for letter in message:
        if letter in letterCount:
            letterCount[letter] +=1
        else:
            letterCount[letter] = 1
            lettersInText+=letter

    return letterCount, lettersInText

def getItemAtIndexZero(items:tuple):
    """Возвращает первый элемент кортежа"""
    return items[0]

def getFrequencyOrder(messsage:str) -> str:
    """
    Возвращает буквы, отсортированные по убыванию частоты встречаемости
    message: Текст для анализа
    """
    letterToFreq, lettersInText= getLetterCount(messsage)
    
    freqToLetter = {}
    for letter in lettersInText:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)
    for freq in freqToLetter:
        freqToLetter[freq] = ''.join(freqToLetter[freq])
    
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)
    saveStatistics(freqPairs, len(messsage))
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)

def main():
    """Основная функция программы"""
    path = ".\\lab_1\\task_2\\cod13.txt"
    text = read_file(path)
    cleanedText = text.replace('\n','').replace('\t','').replace(' ', '')
    frequencyOrder = getFrequencyOrder(cleanedText) #отсортированный по частоте список использованных в тексте букв
    key = {'-': ' ',    
    'U': 'О',
    'd': 'Е',
    'M': 'И',
    'B': 'Т',
    'Y': 'А',
    '3': 'С',
    '>': 'Н',
    'E': 'В',
    '9': 'Р',
    't': 'Л',
    '8': 'Ы',
    'A': 'К',
    'I': 'Д',
    'K': 'М',
    '!': 'Б',
    'Q': 'П',
    'h': 'У',
    'P': 'Я',
    'J': 'З',
    '=': 'Ц',
    'L': 'Ч',
    '$': 'Х',
    'C': 'Ю',
    'G': 'Ь',
    'W': 'Й',
    'V': 'Э',
    'F': 'Ш',
    'R': 'Г',
    'n': 'Щ',
    'Z': 'Ж',
    'O': 'Ф',
    'x': 'Ъ' }

    saveKey(key)
    dechiper_text = ""
    for latter in cleanedText:
        dechiper_text+=key[latter]
    saveResult(dechiper_text)

if __name__ == '__main__':
    """Точка входа в программу"""
    main()
# polybiusCipher.py
import json
import os
import sys

from config import TableSize


def loadKeyFromFile(fileName):
    if not os.path.exists(fileName):
        raise FileNotFoundError(f"Файл {fileName} не найден")
    
    with open(fileName, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    lines = [line.strip() for line in lines if line.strip()]
    
    table = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) > 1:
            row = parts[1:]
            table.append(row)
    
    if len(table) != TableSize:
        print(f"Ошибка: в файле {len(table)} строк, требуется {TableSize}")
        return None, None
    
    encryptDict = {}
    alphabet = ""
    
    for i in range(TableSize):
        if len(table[i]) != TableSize:
            print(f"Ошибка: в строке {i+1} {len(table[i])} элементов, нужно {TableSize}")
            return None, None
        
        for j in range(TableSize):
            char = table[i][j]
            if char != '*':
                if char == '_':
                    encryptDict[' '] = f"{i+1}{j+1}"
                    alphabet += ' '
                else:
                    encryptDict[char] = f"{i+1}{j+1}"
                    alphabet += char
    
    return encryptDict, alphabet


def readOriginalText(fileName):
    if not os.path.exists(fileName):
        raise FileNotFoundError(f"Файл {fileName} не найден")
    
    with open(fileName, 'r', encoding='utf-8') as f:
        text = f.read()
    
    return text.upper()


def saveKeyToJson(fileName, encryptDict):
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(encryptDict, f, ensure_ascii=False, indent=2)


def showKeyContent(fileName):
    print("\nСодержимое key.txt:")
    with open(fileName, 'r', encoding='utf-8') as f:
        print(f.read())


def main():
    try:
        print("\nЗагрузка ключа из key.txt...")
        encryptDict, alphabet = loadKeyFromFile('key.txt')
        
        if encryptDict is None:
            print("Ошибка загрузки ключа")
            sys.exit(1)
        
        print(f"Ключ загружен, символов: {len(encryptDict)}")
        print(f"Алфавит: {alphabet}")
        
        print("Сохранение ключа в key.json")
        saveKeyToJson('key.json', encryptDict)
        
        showKeyContent('key.txt')
        
        print("\nЧтение original.txt...")
        originalText = readOriginalText('original.txt')
        print("Исходный текст:")
        print(originalText)
        print(f"Длина: {len(originalText)} символов\n")
            
    except FileNotFoundError as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
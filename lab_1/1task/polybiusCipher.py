import json
import os
import sys

from config import TableSize


def loadKeyFromFile(fileName):
    """Загружает ключ из файла и создает словарь соответствия символов координатам."""
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
    """Читает исходный текст из файла и возвращает его в верхнем регистре."""
    if not os.path.exists(fileName):
        raise FileNotFoundError(f"Файл {fileName} не найден")
    
    with open(fileName, 'r', encoding='utf-8') as f:
        text = f.read()
    
    return text.upper()


def saveKeyToJson(fileName, encryptDict):
    """Сохраняет ключ в JSON файл."""
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(encryptDict, f, ensure_ascii=False, indent=2)


def encryptText(text, encryptDict):
    """Шифрует текст, заменяя каждый символ на координаты из ключа."""
    result = []
    
    for char in text:
        result.append(encryptDict[char])
    
    return ' '.join(result)


def decryptText(encryptedText, encryptDict):
    """Расшифровывает текст, заменяя координаты обратно на символы."""
    decryptDict = {v: k for k, v in encryptDict.items()}
    pairs = encryptedText.split(' ')
    result = []
    
    for pair in pairs:
        result.append(decryptDict[pair])
    
    return ''.join(result)


def saveToFile(fileName, content):
    """Сохраняет содержимое в файл."""
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(content)


def showKeyContent(fileName):
    """Выводит содержимое файла с ключом на экран."""
    print("\nСодержимое key.txt:")
    with open(fileName, 'r', encoding='utf-8') as f:
        print(f.read())


def main():
    """Основная функция программы: загрузка ключа, шифрование, дешифрование и проверка."""
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
        
        encryptedText = encryptText(originalText, encryptDict)
        decryptedText = decryptText(encryptedText, encryptDict)
        
        saveToFile('encrypted.txt', encryptedText)
        
        print("Зашифрованный текст (encrypted.txt):")
        print(encryptedText)
        print(f"\nПар координат: {len(encryptedText.split())}\n")
        
        print("Расшифрованный текст:")
        print(decryptedText)
        print(f"Символов: {len(decryptedText)}\n")
        
        if originalText == decryptedText:
            print("Шифрование работает корректно")
        else:
            print("Ошибка: расшифровка не совпадает с оригиналом")
            
    except FileNotFoundError as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

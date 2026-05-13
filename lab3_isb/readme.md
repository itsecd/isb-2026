Лабораторная работа: реализация гибридной криптосистемы.

Используется:
- AES-CBC для шифрования файла
- RSA-OAEP SHA-256 для шифрования AES-ключа
- AES-ключи: 128 / 192 / 256 бит

Режимы работы/сценарии:

- Генерация ключей: python main.py gen --config comands.json


- Шифрование: python main.py enc --config comands.json


- Дешифрование: python main.py dec --config comands.json


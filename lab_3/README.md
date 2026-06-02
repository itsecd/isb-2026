# Лабораторная работа №3: Гибридная криптосистема
**Вариант:** 9  
**Алгоритм:** IDEA (128 бит) + RSA (2048 бит)  
**Студент:** Родионов Антон 6214-100503D

## Структура проекта
- `main.py` — точка входа, парсинг аргументов
- `services.py` — основные функции (генерация, шифрование, дешифрование)
- `asymmetric.py` — работа с RSA
- `symmetric.py` — работа с IDEA
- `utils.py` — утилиты для работы с файлами
- `settings.json` — конфигурация путей

## Установка
```bash
pip install -r requirements.txt
```

Использование
1. Генерация ключей
```bash
python hybrid_crypto.py -gen --sym-key keys/sym.enc --pub-key keys/pub.pem --priv-key keys/priv.pem
```
2. Шифрование
```bash
python hybrid_crypto.py -enc --input data.txt --output data.enc --enc-sym-key keys/sym.enc --priv-key keys/priv.pem
```
3. Дешифрование
```bash
python hybrid_crypto.py -dec --input data.enc --output restored.txt --enc-sym-key keys/sym.enc --priv-key keys/priv.pem
```
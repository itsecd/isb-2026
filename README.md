# Лабораторная работа №3

## Построение гибридной криптосистемы

Вариант 4: симметричный алгоритм 3DES, ключ 64/128/192 бит с пользовательским выбором длины.

Гибридная система объединяет:

- RSA-2048 с OAEP/SHA-256 для шифрования ключа симметричного алгоритма;
- 3DES в режиме CBC для шифрования файлов;
- ANSI X.923 padding для выравнивания данных до размера блока 3DES.

## Структура

```text
lab_3/
├── main.py                    # CLI
├── config.py                  # чтение JSON-настроек
├── file_utils.py              # работа с файлами
├── rsa_utils.py               # RSA-ключи и RSA-OAEP
├── triple_des.py              # 3DES/CBC и padding
├── hybrid_system.py           # сценарии лабораторной
├── settings_generation.json   # пример настроек генерации ключей
├── settings_encrypt.json      # пример настроек шифрования
├── settings_decrypt.json      # пример настроек дешифрования
├── requirements.txt
├── data/
└── tests/
```

## Установка

```bash
cd lab_3
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

Сгенерировать ключи гибридной системы:

```bash
python main.py -gen -c settings_generation.json
```

Зашифровать файл:

```bash
python main.py -enc -c settings_encrypt.json
```

Расшифровать файл:

```bash
python main.py -dec -c settings_decrypt.json
```

Параметры можно передавать и без JSON:

```bash
python main.py -gen --key-bits 192 --encrypted-symmetric-key data/symmetric.enc --public-key data/public.pem --private-key data/private.pem
python main.py -enc --input-file data/input.txt --private-key data/private.pem --encrypted-symmetric-key data/symmetric.enc --output-file data/encrypted.bin
python main.py -dec --input-file data/encrypted.bin --private-key data/private.pem --encrypted-symmetric-key data/symmetric.enc --output-file data/decrypted.txt
```

## Проверка

Функциональный тест выполняет полный цикл генерации ключей, шифрования и дешифрования:

```bash
cd lab_3
python -m unittest discover -s tests
```

После ручного запуска можно сравнить файлы `data/input.txt` и `data/decrypted.txt`: содержимое должно совпадать.

## Краткая справка о 3DES

3DES (Triple DES, TDEA) появился как развитие DES после того, как исходный 56-битный ключ DES стал недостаточно стойким к перебору. Идея тройного применения DES была предложена в 1970-х годах Уолтером Тачманом из IBM как совместимый способ усилить DES без проектирования полностью нового блочного шифра.

Алгоритм применяет DES три раза к одному 64-битному блоку данных и поддерживает варианты с двумя или тремя ключами. В терминах библиотеки `cryptography` это ключи длиной 64, 128 или 192 бит, включая служебные биты четности DES.

3DES долго использовался в банковских и платежных системах и был стандартизован NIST как TDEA. Сейчас алгоритм считается устаревшим: размер блока 64 бита делает его уязвимым для атак на большие объемы данных, включая Sweet32, а скорость работы ниже, чем у современных алгоритмов. Документ NIST SP 800-67 Rev. 2 был отозван 1 января 2024 года, поэтому TDEA больше не является одобренным NIST блочным шифром для новых федеральных применений: https://csrc.nist.gov/pubs/sp/800/67/r2/final

Для новых систем рекомендуется AES, но 3DES остается полезным учебным примером блочного шифра и гибридной криптосистемы.

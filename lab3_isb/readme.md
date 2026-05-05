Лабораторная работа: реализация гибридной криптосистемы.

Используется:
- AES-CBC для шифрования файла
- RSA-OAEP SHA-256 для шифрования AES-ключа
- AES-ключи: 128 / 192 / 256 бит

Режимы работы/сценарии:

- Генерация ключей: python main.py gen --ENC_PATH encrypted_aes_key.bin --OPN_KEY_PATH public.pem --PRV_KEY_PATH private.pem --SIZE 256


- Шифрование: python main.py enc --TXT_PATH text.txt --PRV_ASYM_KEY_PATH private.pem --ENC_KEY_PATH encrypted_aes_key.bin --ENC_TXT_PATH encrypted_text.bin


- Дешифрование: python main.py dec --ENC_TXT_PATH encrypted_text.bin --PRV_ASYM_KEY_PATH private.pem --ENC_KEY_PATH encrypted_aes_key.bin --DEC_TXT_PATH decrypted_text.txt



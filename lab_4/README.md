# Лабораторная работа №4 — «Хеш-функции»
## Вариант 4: Использование HMAC для проверки подлинности сообщений

---

## Цель работы

Изучить механизм HMAC (Hash-based Message Authentication Code) и реализовать систему проверки подлинности сообщений с графическим интерфейсом, CLI-параметрами и визуализацией коллизий.

---

## Структура проекта

```
lab4_hmac/
├── main.py                  # Точка входа
├── modules/
│   ├── __init__.py
│   ├── logger.py            # Настройка логгера
│   ├── env_parser.py        # Загрузка параметров из .env
│   ├── hmac_core.py         # Генерация, верификация, tamper-detection
│   ├── collision.py         # Поиск частичной коллизии (tqdm)
│   └── gui.py               # PyQt6 GUI
├── tests/
│   ├── __init__.py
│   └── test_hmac.py         # Юнит-тесты
├── .env.example
├── requirements.txt
└── README.md
```

---

## Установка

```bash
pip install -r requirements.txt
```

---

## Запуск

### Интерактивное меню
```bash
python main.py
```

### Графический интерфейс (PyQt6)
```bash
python main.py --gui
```

### CLI — подпись сообщения
```bash
python main.py sign "Hello, world!" -k mysecret -o signed.json
```

### CLI — верификация
```bash
python main.py verify signed.json -k mysecret
```

### CLI — tamper-проверка
```bash
python main.py tamper signed.json "Hacked message" -k mysecret
```

### CLI — поиск коллизии (24-битный префикс)
```bash
python main.py collision -b 24 -k mysecret
```

### Юнит-тесты
```bash
python -m pytest tests/ -v
```

---

## Теоретическая справка

### Что такое HMAC?

HMAC — механизм аутентификации сообщений на основе хеш-функции и секретного ключа.  
Формула: `HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m))`

### Чем HMAC отличается от обычного хеша?

Обычный хеш (`SHA-256(m)`) не требует ключа и не даёт гарантий подлинности — любой может пересчитать его для изменённого сообщения. HMAC без знания секретного ключа невозможно подделать.

### Для чего используется секретный ключ?

Ключ гарантирует, что только стороны, знающие его, могут сформировать или проверить тег. Это предотвращает атаки подмены, когда злоумышленник изменяет сообщение и пересчитывает тег.

### Где применяется HMAC?

- Проверка целостности JWT-токенов (`HS256`).
- Подпись webhook-запросов (GitHub, Stripe и др.).
- Протоколы TLS/SSL для проверки рукопожатия.
- API-аутентификация (AWS Signature v4, и др.).

### Почему HMAC защищает от подмены данных?

Без секретного ключа вычислить корректный HMAC для изменённого сообщения вычислительно неосуществимо. Функция `hmac.compare_digest` защищает от атак по времени (timing attacks).

---

## Описание модулей

### `hmac_core.py`

| Функция | Описание |
|---|---|
| `compute_hmac(message, key, algo)` | Вычисляет HMAC-тег |
| `verify_hmac(message, key, tag, algo)` | Проверяет тег; использует `compare_digest` |
| `sign_and_save(message, key, path, algo)` | Сохраняет подписанный конверт в JSON |
| `load_and_verify(path, key)` | Загружает конверт и проверяет тег |
| `tamper_and_verify(path, key, tampered)` | Проверяет изменённое сообщение против оригинального тега |

Поддерживаемые алгоритмы: `sha256`, `sha512`, `sha3_256`, `sha3_512`.

### `collision.py`

Реализует атаку «День рождения» на усечённый тег HMAC-SHA256.  
Прогресс поиска визуализируется через `tqdm` в терминале.  
Рекомендуемый диапазон: 16–28 бит (компромисс между наглядностью и временем).

### `gui.py`

Четыре вкладки PyQt6:

| Вкладка | Функция |
|---|---|
| Generate | Подписать сообщение и сохранить конверт |
| Verify | Загрузить и верифицировать конверт |
| Tamper | Проверить обнаружение подмены |
| Collision | Запустить поиск частичной коллизии |

---

## Результаты выполнения

### Подпись и верификация

```
$ python main.py sign "Test message" -k secret123 -o signed.json
[+] Signed envelope saved → signed.json
    HMAC : 3f2a1b...

$ python main.py verify signed.json -k secret123
[+] VALID — message: 'Test message'
```

### Обнаружение подмены

```
$ python main.py tamper signed.json "Malicious payload" -k secret123
[+] Tampering detected — message correctly rejected.
```

### Коллизия (24-битный префикс)

```
Collision search (24-bit prefix): 100%|████████| 14523/14523 [00:01<00:00]
[+] Collision found!
    Message A : aB3kLpQr
    Message B : xZ9mNvKw
    Shared prefix : 0xa3f2c1
```

Ожидаемое число попыток до коллизии при n-битном префиксе: ~`2^(n/2)` (парадокс дня рождения).

---

## Вывод

Реализована полноценная система аутентификации сообщений на основе HMAC-SHA256. Продемонстрированы: корректное обнаружение подмены, защита от timing-атак через `hmac.compare_digest`, визуализация атаки «День рождения» на усечённый тег. Приложение покрыто юнит-тестами, имеет GUI на PyQt6 и полноценный CLI через `argparse`.

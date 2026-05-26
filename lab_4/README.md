# Лабораторная работа №4

## Функции
- SHA-256 хеширование файла
- сохранение контрольной суммы
- проверка целостности
- вывод `OK/FAILED`
- запись результата проверки в файл
- GUI на PyQt6
- CLI через argparse
- демонстрация подбора коллизии через tqdm
- юнит-тесты

## Установка
```bash
pip install -r requirements.txt
```

## Запуск CLI
```bash
python main.py save test_file.txt
python main.py verify test_file.txt
python main.py collide
```

## Запуск GUI
```bash
python gui.py
```

## Тесты
```bash
python tests.py
```
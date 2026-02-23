from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, Tuple


def read_cipher_text(filepath: str | Path, keep_newlines: bool = False) -> str:
    """Считывает шифртекст из файла."""
    path = Path(filepath)
    text = path.read_text(encoding="utf-8")
    if not keep_newlines:
        text = text.replace("\n", "")
    return text


def frequency_analysis(text: str, top_n: int | None = 10) -> Tuple[Counter, str]:
    """Выполняет частотный анализ текста."""
    freq = Counter(text)
    items = freq.most_common() if top_n is None else freq.most_common(top_n)

    lines = []
    lines.append("Частота символов:")
    lines.append("-" * 30)
    for ch, count in items:
        lines.append(f"{repr(ch)}: {count}")
    report = "\n".join(lines)
    return freq, report


def write_frequency_report(
    freq: Counter,
    filepath: str | Path,
    *,
    include_total: bool = True,
    sort_by: str = "count_desc",
) -> None:
    """Сохраняет таблицу частот символов в файл."""
    path = Path(filepath)

    if sort_by == "count_desc":
        rows = freq.most_common()
    elif sort_by == "symbol_asc":
        rows = sorted(freq.items(), key=lambda x: x[0])
    else:
        raise ValueError("sort_by must be 'count_desc' or 'symbol_asc'")

    lines = []
    lines.append("Частотный анализ (символ -> количество)")
    lines.append("=" * 45)
    for ch, count in rows:
        lines.append(f"{repr(ch)}\t{count}")

    if include_total:
        lines.append("-" * 45)
        lines.append(f"TOTAL_LEN\t{sum(freq.values())}")
        lines.append(f"UNIQUE_CHARS\t{len(freq)}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_replacements(text: str, replacements: Dict[str, str]) -> str:
    """Применяет таблицу замен символов к тексту."""
    for old, new in replacements.items():
        if len(old) != 1 or len(new) != 1:
            raise ValueError("All replacement keys/values must be single characters.")

    modified = text
    for old, new in replacements.items():
        modified = modified.replace(old, new)
    return modified


def interactive_replace_symbols(cipher_text: str) -> None:
    """Запускает интерактивный режим замены символов."""
    print("=== ПРОГРАММА ЗАМЕНЫ СИМВОЛОВ ===")
    print(cipher_text)

    replacements: Dict[str, str] = {}

    while True:
        print("\n" + "=" * 50)
        print("Текущие замены:")
        if replacements:
            for old, new in replacements.items():
                print(f"  '{old}' -> '{new}'")
        else:
            print("  Замен пока нет")

        print("\nВыберите действие:")
        print("1. Добавить/изменить замену")
        print("2. Показать текст с текущими заменами")
        print("3. Сбросить все замены")
        print("4. Сохранить результат в файл")
        print("5. Выйти")

        choice = input("\nВаш выбор (1-5): ").strip()

        if choice == "1":
            old_symbol = input("Введите символ, который нужно заменить: ")
            if len(old_symbol) != 1:
                print("Ошибка: введите один символ!")
                continue

            new_symbol = input("Введите символ для замены: ")
            if len(new_symbol) != 1:
                print("Ошибка: введите один символ!")
                continue

            replacements[old_symbol] = new_symbol
            print(f"Замена '{old_symbol}' -> '{new_symbol}' добавлена")

        elif choice == "2":
            if not replacements:
                print("Нет замен для применения!")
                continue

            modified_text = apply_replacements(cipher_text, replacements)

            print("\n" + "=" * 50)
            print("ТЕКСТ ПОСЛЕ ВСЕХ ЗАМЕН:")
            print("=" * 50)
            print(modified_text)

        elif choice == "3":
            replacements.clear()
            print("Все замены сброшены")

        elif choice == "4":
            if not replacements:
                print("Нет замен для сохранения!")
                continue

            modified_text = apply_replacements(cipher_text, replacements)

            filename = input(
                "Введите имя файла для сохранения (по умолчанию: replaced_text.txt): "
            ).strip()
            if not filename:
                filename = "replaced_text.txt"

            Path(filename).write_text(modified_text, encoding="utf-8")
            print(f"Текст сохранен в файл: {filename}")

        elif choice == "5":
            print("Программа завершена")
            break

        else:
            print("Неверный выбор, попробуйте снова")


def main() -> None:
    """Запускает полный процесс анализа и интерактивной расшифровки."""
    input_file = input("Путь к файлу с cipher_text (по умолчанию: cipher_text.txt): ").strip()
    if not input_file:
        input_file = "cipher_text.txt"

    cipher_text = read_cipher_text(input_file, keep_newlines=False)

    freq, report = frequency_analysis(cipher_text, top_n=10)
    print(report)

    out_file = input(
        "Файл для сохранения частот (по умолчанию: freq_report.txt): "
    ).strip()
    if not out_file:
        out_file = "freq_report.txt"

    write_frequency_report(freq, out_file, include_total=True, sort_by="count_desc")
    print(f"Частоты сохранены в файл: {out_file}")

    interactive_replace_symbols(cipher_text)


if __name__ == "__main__":
    main()
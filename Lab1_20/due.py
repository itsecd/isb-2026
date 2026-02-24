from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, Tuple


def load_encrypted_data(file_path: str | Path, preserve_linebreaks: bool = False) -> str:
    """Загружает зашифрованный текст из указанного файла."""
    target_path = Path(file_path)
    raw_content = target_path.read_text(encoding="utf-8")
    if not preserve_linebreaks:
        raw_content = raw_content.replace("\n", "")
    return raw_content


def perform_symbol_analysis(input_text: str, limit_results: int | None = 10) -> Tuple[Counter, str]:
    """Проводит подсчет частоты встречаемости символов."""
    symbol_counter = Counter(input_text)
    top_symbols = symbol_counter.most_common() if limit_results is None else symbol_counter.most_common(limit_results)

    output_lines = []
    output_lines.append("Статистика встречаемости символов:")
    output_lines.append("-" * 30)
    for character, occurrence in top_symbols:
        output_lines.append(f"{repr(character)}: {occurrence}")
    formatted_report = "\n".join(output_lines)
    return symbol_counter, formatted_report


def export_frequency_table(
    symbol_data: Counter,
    output_path: str | Path,
    *,
    add_summary: bool = True,
    sort_criteria: str = "by_frequency",
) -> None:
    """Экспортирует результаты частотного анализа в текстовый файл."""
    destination = Path(output_path)

    if sort_criteria == "by_frequency":
        data_rows = symbol_data.most_common()
    elif sort_criteria == "by_symbol":
        data_rows = sorted(symbol_data.items(), key=lambda pair: pair[0])
    else:
        raise ValueError("sort_criteria должен быть 'by_frequency' или 'by_symbol'")

    report_lines = []
    report_lines.append("Результаты анализа частоты символов")
    report_lines.append("=" * 45)
    for character, frequency in data_rows:
        report_lines.append(f"{repr(character)}\t{frequency}")

    if add_summary:
        report_lines.append("-" * 45)
        report_lines.append(f"ОБЩАЯ_ДЛИНА\t{sum(symbol_data.values())}")
        report_lines.append(f"УНИКАЛЬНЫХ\t{len(symbol_data)}")

    destination.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def perform_substitutions(original_text: str, substitution_rules: Dict[str, str]) -> str:
    """Выполняет замену символов согласно заданным правилам."""
    for source, target in substitution_rules.items():
        if len(source) != 1 or len(target) != 1:
            raise ValueError("Все ключи и значения замен должны быть одиночными символами.")

    processed_text = original_text
    for source, target in substitution_rules.items():
        processed_text = processed_text.replace(source, target)
    return processed_text


def start_interactive_mode(encrypted_content: str) -> None:
    """Запускает интерактивный режим подбора замен."""
    print("=== СИСТЕМА РАСШИФРОВКИ ТЕКСТА ===")
    print(encrypted_content)

    substitution_map: Dict[str, str] = {}

    while True:
        print("\n" + "=" * 50)
        print("Текущие подстановки:")
        if substitution_map:
            for source, target in substitution_map.items():
                print(f"  '{source}' -> '{target}'")
        else:
            print("  Подстановки отсутствуют")

        print("\nДоступные операции:")
        print("1. Добавить/изменить правило замены")
        print("2. Показать текст с примененными заменами")
        print("3. Сбросить все правила")
        print("4. Сохранить результат в файл")
        print("5. Выйти из программы")

        user_choice = input("\nВаш выбор (1-5): ").strip()

        if user_choice == "1":
            source_char = input("Введите символ, который нужно заменить: ")
            if len(source_char) != 1:
                print("Ошибка: необходимо ввести один символ!")
                continue

            target_char = input("Введите символ для подстановки: ")
            if len(target_char) != 1:
                print("Ошибка: необходимо ввести один символ!")
                continue

            substitution_map[source_char] = target_char
            print(f"Правило '{source_char}' -> '{target_char}' добавлено")

        elif user_choice == "2":
            if not substitution_map:
                print("Нет правил для применения!")
                continue

            transformed_text = perform_substitutions(encrypted_content, substitution_map)

            print("\n" + "=" * 50)
            print("РЕЗУЛЬТАТ ПРИМЕНЕНИЯ ПОДСТАНОВОК:")
            print("=" * 50)
            print(transformed_text)

        elif user_choice == "3":
            substitution_map.clear()
            print("Все правила замены удалены")

        elif user_choice == "4":
            if not substitution_map:
                print("Нет данных для сохранения!")
                continue

            transformed_text = perform_substitutions(encrypted_content, substitution_map)

            output_filename = input(
                "Укажите имя файла для сохранения (по умолчанию: transformed_output.txt): "
            ).strip()
            if not output_filename:
                output_filename = "transformed_output.txt"

            Path(output_filename).write_text(transformed_text, encoding="utf-8")
            print(f"Результат сохранен в файл: {output_filename}")

        elif user_choice == "5":
            print("Работа программы завершена")
            break

        else:
            print("Некорректный выбор, повторите попытку")


def run_application() -> None:
    """Запускает основной рабочий процесс: анализ и интерактивную расшифровку."""
    source_file = input("Путь к файлу с зашифрованным текстом (по умолчанию: encrypted_data.txt): ").strip()
    if not source_file:
        source_file = "encrypted_data.txt"

    encrypted_data = load_encrypted_data(source_file, preserve_linebreaks=False)

    frequencies, analysis_output = perform_symbol_analysis(encrypted_data, limit_results=10)
    print(analysis_output)

    result_file = input(
        "Файл для сохранения результатов анализа (по умолчанию: symbol_stats.txt): "
    ).strip()
    if not result_file:
        result_file = "symbol_stats.txt"

    export_frequency_table(frequencies, result_file, add_summary=True, sort_criteria="by_frequency")
    print(f"Статистика символов сохранена в файл: {result_file}")

    start_interactive_mode(encrypted_data)


if __name__ == "__main__":
    run_application()
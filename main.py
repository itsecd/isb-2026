import sys
from cli import run_cli
from gui import run_gui


def main() -> None:
    """
    Главная точка входа в программный комплекс.

    Анализирует параметры командной строки `sys.argv`. Если передан хотя бы один
    аргумент (помимо имени самого скрипта), перенаправляет поток управления в консольный
    интерфейс CLI. В противном случае инициализирует графическую оболочку GUI.

    Raises:
        Exception: Для перехвата любых непредвиденных сбоев на уровне работы приложения.
    """
    try:
        if len(sys.argv) > 1:
            run_cli()
        else:
            run_gui()
    except Exception as err:
        print(
            f"Критический сбой работы приложения! Unexpected {err=}, {type(err)=}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()

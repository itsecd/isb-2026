import traceback

from file_utils import load_config
from gui import run_gui


def main() -> None:
    """
    Точка входа в программу.
    Загружает конфигурацию из settings.json
    и запускает графический интерфейс.
    """
    try:
        config = load_config("settings.json")
        run_gui(config)

    except Exception:
        print("[ERROR] Произошла ошибка при запуске программы:")
        traceback.print_exc()


if __name__ == "__main__":
    main()

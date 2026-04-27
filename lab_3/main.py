from file_utils import load_config
from gui import run_gui


def main() -> None:
    """
    Точка входа в программу.
    Загружает конфигурацию и запускает GUI.
    """
    try:
        config = load_config()
        run_gui(config)

    except Exception:
        import traceback

        print("[ERROR] Произошла ошибка при запуске программы:")
        traceback.print_exc()


if __name__ == "__main__":
    main()

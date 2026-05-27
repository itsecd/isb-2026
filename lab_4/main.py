import hashing
from hashing import serialize


def main(settings: dict[str, str | int | bytes]) -> None:
    """
    Точка входа в логику программы
    Args:
        settings (dict): Параметры приложения
    """
    hash_db = hashing.load_checksums(settings)
    serialize(data=json.dumps(hash_db, indent=2).encode('utf-8'), path=settings["hash_db_path"])



if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--settings", help="Путь до файла с параметрами", default="./settings.json")

    args = parser.parse_args()

    try:
        with open(args.settings, mode="r", encoding="utf-8") as input:
            settings = json.load(input)
        main(settings)
    except FileNotFoundError as e:
        print(f"Файл {e.filename} не найден!")
    except Exception as e:
        print(e)
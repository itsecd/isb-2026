import json


def load_config(path):

    try:

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:

        raise FileNotFoundError(
            f"Файл конфигурации не найден: {path}"
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            f"Ошибка JSON: {error}"
        )
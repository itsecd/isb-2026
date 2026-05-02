import json


def load_config(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(path, config):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

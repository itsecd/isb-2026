import task1.work_file as work_file


def get_frequency(text: str) -> dict:
    fre_dict = {}
    size = len(text)
    for i in text:
        fre_dict[i] = fre_dict.get(i, 0) + 1
    for i in fre_dict:
        fre_dict[i] = fre_dict[i] / size
    return fre_dict


def get_key(dict_fi: dict, dict_se:dict) -> dict:
    new_dict = {}

    for key1, key2 in zip(dict_fi.keys(), dict_se.keys()):
        new_dict[key1] = key2
    return new_dict



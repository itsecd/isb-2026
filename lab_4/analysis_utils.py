def count_bit_diff(h1: str, h2: str):
    """
    Подсчет количества различающихся бит между двумя хешами.

    Шестнадцатеричные строки хешей переводятся в целочисленный формат.
    С помощью XOR вычисляются и далее подсчитываются разные биты.

    Args:
        h1: Первая строка хеша.
        h2: Вторая строка хеша.

    Returns:
        Целое число, количество различающихся бит.

    Raises:
        ValueError: Если один из хешей пуст, хеши имеют разный размер или формат хешей некорректен.
    """
    if not h1 or not h2:
        raise ValueError("Пустой хеш")

    if len(h1) != len(h2):
        raise ValueError("Хеши имеют разный размер")

    try:
        x1 = int(h1, 16)
        x2 = int(h2, 16)
    except ValueError:
        raise ValueError("Некорректный шестнадцатеричный формат")

    return (x1 ^ x2).bit_count()


def diff_percent(diff_bits: int, total_bits: int):
    """
    Вычисление процента изменившихся бит.

    Args:
        diff_bits: Количество изменённых бит.
        total_bits: Общее количество бит.

    Returns:
        Вещественное число, процент изменений.

    Raises:
        ValueError: Если общее количество бит равно нулю или измененных бит больше общего количества.
    """
    if total_bits == 0:
        raise ValueError("Неверное общее количество бит")

    if diff_bits > total_bits:
        raise ValueError("Количество измененных бит не может превышать общее количество бит")

    return (diff_bits / total_bits) * 100

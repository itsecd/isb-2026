import random

def change_one_char(s: str):
    """
    Изменение одного случайного символа в строке.

    Для замены используется стандартный диапазон печатных символов таблицы ASCII.
    С помощью циклического сдвига новый символ всегда отличается от старого.

    Args:
        s: Исходная строка.

    Returns:
        Измененный массив байтов (bytes).

    Raises:
        ValueError: Если строка пуста.
    """
    if not s:
        raise ValueError("Строка пуста")

    index = random.randint(0, len(s) - 1)
    old_code = ord(s[index])

    if 32 <= old_code <= 126:
        shift = random.randint(1, 94)
        new_code = 32 + (old_code - 32 + shift) % 95
    else:
        new_code = random.randint(32, 126)

    new_char = chr(new_code)
    modified_str = s[:index] + new_char + s[index + 1:]

    return modified_str.encode("utf-8")


def change_one_bit(s: str):
    """
    Изменение одного случайного бита.

    Случайно выбирается 1 байт и 1 бит в этом байте (справа налево).
    С помощью << формируется двоичный код, где только 1 бит = 1.
    Далее XOR инвертирует выбранный бит.

    Args:
        s: Исходная строка.

    Returns:
        Измененный массив байтов (bytes).

    Raises:
        ValueError: Если строка пуста.
    """
    if not s:
        raise ValueError("Строка пуста")

    data = bytearray(s.encode("utf-8"))

    byte_index = random.randint(0, len(data) - 1)
    bit_index = random.randint(0, 7)

    data[byte_index] ^= (1 << bit_index)

    return bytes(data)


def change_register(s: str):
    """
    Изменение регистра одной случайной буквы в строке.

    Случайно выбранная буква меняет регистр на противоположный.
    Если букв нет, возвращаем исходную строку.

    Args:
        s: Исходная строка.

    Returns:
        Измененный массив байтов (bytes).

    Raises:
        ValueError: Если строка пуста.
    """
    if not s:
        raise ValueError("Строка пуста")

    letters = [i for i, c in enumerate(s) if c.isalpha()]

    if not letters:
        return s.encode("utf-8")
        
    index = random.choice(letters)
    c = s[index]

    new_c = c.upper() if c.islower() else c.lower()
    modified_str = s[:index] + new_c + s[index + 1:]

    return modified_str.encode("utf-8")


def apply_mutation(text: str, mode: str):
    """
    Применение выбранного типа мутации к исходному тексту.

    Args:
        text: Исходная строка для мутации.
        mode: Режим мутации ("char", "bit" или "reg").

    Returns:
        Кортеж (измененный_массив_байтов, название_операции_на_русском).

    Raises:
        ValueError: Если передан неизвестный режим операции.
    """
    match mode:
        case "char":
            return change_one_char(text), "Символ"
        case "bit":
            return change_one_bit(text), "Бит"
        case "reg":
            return change_register(text), "Регистр"
        case _:
            raise ValueError("Неизвестная операция")

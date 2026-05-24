import hashlib
import random
import string
from dataclasses import dataclass


@dataclass
class AvalancheResult:
    """Результат одного эксперимента по лавинному эффекту."""
    original_text: str
    modified_text: str
    modification_type: str          
    original_hash: str
    modified_hash: str
    changed_bits: int
    total_bits: int
    diff_percent: float



def compute_hash(text: str, algorithm: str = "sha256") -> str:
    """
    Вычислить хеш строки
    """
    supported = {"sha256", "sha1", "md5", "sha3_256"}
    if algorithm not in supported:
        raise ValueError(f"Неподдерживаемый алгоритм '{algorithm}'. Доступны: {supported}")
    h = hashlib.new(algorithm, text.encode("utf-8"))
    return h.hexdigest()


def hash_to_bits(hex_digest: str) -> str:
    """Преобразовать в двоичную строку."""
    return bin(int(hex_digest, 16))[2:].zfill(len(hex_digest) * 4)


def count_differing_bits(hash1: str, hash2: str) -> int:
    """
    Подсчитать количество различающихся бит
    """
    if len(hash1) != len(hash2):
        raise ValueError("Длины хешей не совпадают.")
    bits1 = hash_to_bits(hash1)
    bits2 = hash_to_bits(hash2)
    return sum(b1 != b2 for b1, b2 in zip(bits1, bits2))


def diff_percent(changed: int, total: int) -> float:
    """Процент изменённых бит."""
    if total == 0:
        return 0.0
    return round(changed / total * 100, 2)


def change_one_char(text: str, position: int | None = None) -> tuple[str, int]:
    """
    Заменить один символ на другой
    """
    if not text:
        raise ValueError("Строка не должна быть пустой.")
    if position is None:
        position = random.randint(0, len(text) - 1)
    position = position % len(text)
    old_char = text[position]
    alphabet = string.ascii_letters + string.digits
    candidates = [c for c in alphabet if c != old_char]
    new_char = random.choice(candidates)
    modified = text[:position] + new_char + text[position + 1:]
    return modified, position


def change_one_bit(text: str, byte_index: int | None = None, bit_index: int | None = None) -> tuple[str, int, int]:
    """
    Инвертировать один бит в байтовом представлении строки
    """
    if not text:
        raise ValueError("Строка не должна быть пустой.")
    data = bytearray(text.encode("utf-8"))
    if byte_index is None:
        byte_index = random.randint(0, len(data) - 1)
    byte_index = byte_index % len(data)
    if bit_index is None:
        bit_index = random.randint(0, 7)
    bit_index = bit_index % 8
    data[byte_index] ^= (1 << bit_index)
    try:
        modified = data.decode("utf-8")
    except UnicodeDecodeError:
        modified = data.decode("utf-8", errors="replace")
    return modified, byte_index, bit_index


def change_case(text: str, position: int | None = None) -> tuple[str, int]:
    """
    Изменить регистр одной буквы
    """
    letter_positions = [i for i, c in enumerate(text) if c.isalpha()]
    if not letter_positions:
        raise ValueError("В строке нет букв для изменения регистра.")
    if position is None or position not in letter_positions:
        position = random.choice(letter_positions)
    char = text[position]
    new_char = char.lower() if char.isupper() else char.upper()
    modified = text[:position] + new_char + text[position + 1:]
    return modified, position


def run_single_experiment(
    original: str,
    modification: str = "char",
    algorithm: str = "sha256",
) -> AvalancheResult:
    """
    Провести один эксперимент лавинного эффекта
    """
    if modification == "char":
        modified, _ = change_one_char(original)
        mod_label = "Замена символа"
    elif modification == "bit":
        modified, byte_i, bit_i = change_one_bit(original)
        mod_label = f"Инверсия бита (байт {byte_i}, бит {bit_i})"
    elif modification == "case":
        modified, pos = change_case(original)
        mod_label = f"Смена регистра (позиция {pos})"
    else:
        raise ValueError(f"Неизвестный тип модификации: '{modification}'. Ожидается 'char', 'bit' или 'case'.")

    h_orig = compute_hash(original, algorithm)
    h_mod = compute_hash(modified, algorithm)
    changed = count_differing_bits(h_orig, h_mod)
    total = len(hash_to_bits(h_orig))

    return AvalancheResult(
        original_text=original,
        modified_text=modified,
        modification_type=mod_label,
        original_hash=h_orig,
        modified_hash=h_mod,
        changed_bits=changed,
        total_bits=total,
        diff_percent=diff_percent(changed, total),
    )


def run_experiments(
    original: str,
    count: int = 10,
    algorithm: str = "sha256",
    progress_callback=None,
) -> list[AvalancheResult]:
    """
    Провести серию экспериментов по всем трём типам модификаций
    """
    if count < 1:
        raise ValueError("Количество экспериментов должно быть >= 1.")
    modifications = ["char", "bit", "case"]
    results = []
    total_steps = count * len(modifications)
    step = 0
    for mod in modifications:
        for _ in range(count):
            try:
                result = run_single_experiment(original, mod, algorithm)
                results.append(result)
            except ValueError:
                pass  # например, строка без букв для 'case' — пропускаем
            step += 1
            if progress_callback:
                progress_callback(step, total_steps)
    return results


def summarize_results(results: list[AvalancheResult]) -> dict:
    """
    Сводная статистика по списку результатов
    """
    if not results:
        return {}
    percents = [r.diff_percent for r in results]
    bits = [r.changed_bits for r in results]
    by_mod: dict[str, list[float]] = {}
    for r in results:
        by_mod.setdefault(r.modification_type, []).append(r.diff_percent)

    return {
        "total_experiments": len(results),
        "avg_diff_percent": round(sum(percents) / len(percents), 2),
        "min_diff_percent": min(percents),
        "max_diff_percent": max(percents),
        "avg_changed_bits": round(sum(bits) / len(bits), 1),
        "by_modification": {
            mod: round(sum(vals) / len(vals), 2)
            for mod, vals in by_mod.items()
        },
    }

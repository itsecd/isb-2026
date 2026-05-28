import hashlib
import json
import random
import string
from dataclasses import dataclass
from pathlib import Path


def load_config(config_path: str | Path | None = None) -> dict:
    """Загрузить настройки проекта из JSON-файла."""
    path = Path(config_path) if config_path else Path(__file__).with_name("config.json")
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Не найден файл конфигурации: {path}. "
            "Положите config.json рядом с hash_core.py."
        ) from exc


CONFIG = load_config()

HASHING_CONFIG = CONFIG["hashing"]
EXPERIMENT_CONFIG = CONFIG["experiments"]
BITS_CONFIG = CONFIG["bits"]
QUALITY_CONFIG = CONFIG["quality"]
DISPLAY_CONFIG = CONFIG["display"]
GUI_CONFIG = CONFIG["gui"]

DEFAULT_ALGORITHM = HASHING_CONFIG["default_algorithm"]
TEXT_ENCODING = HASHING_CONFIG["text_encoding"]
DECODE_ERRORS = HASHING_CONFIG["decode_errors"]
SUPPORTED_ALGORITHMS = tuple(HASHING_CONFIG["supported_algorithms"])

DEFAULT_EXPERIMENT_COUNT = EXPERIMENT_CONFIG["default_count"]
MIN_EXPERIMENT_COUNT = EXPERIMENT_CONFIG["min_count"]
MAX_EXPERIMENT_COUNT = EXPERIMENT_CONFIG["max_count"]
MODIFICATION_TYPES = tuple(EXPERIMENT_CONFIG["modification_types"])
MODIFICATION_LABELS = EXPERIMENT_CONFIG["modification_labels"]
ALL_MODIFICATIONS = EXPERIMENT_CONFIG["all_modifications_alias"]

BITS_IN_HEX_DIGIT = BITS_CONFIG["hex_digit"]
BITS_IN_BYTE = BITS_CONFIG["byte"]

HASH_PREVIEW_LENGTH = DISPLAY_CONFIG["hash_preview_length"]
TABLE_HASH_PREVIEW_LENGTH = DISPLAY_CONFIG["table_hash_preview_length"]
TEXT_PREVIEW_LENGTH = DISPLAY_CONFIG["text_preview_length"]
PROGRESS_BAR_LENGTH = DISPLAY_CONFIG["progress_bar_length"]
PROGRESS_NCOLS = DISPLAY_CONFIG["progress_ncols"]

EXCELLENT_AVALANCHE_PERCENT = QUALITY_CONFIG["excellent_percent"]
MODERATE_AVALANCHE_PERCENT = QUALITY_CONFIG["moderate_percent"]
WARNING_AVALANCHE_PERCENT = QUALITY_CONFIG["warning_percent"]
IDEAL_AVALANCHE_PERCENT = QUALITY_CONFIG["ideal_percent"]
QUALITY_LEVELS = QUALITY_CONFIG["levels"]

GUI_WINDOW_TITLE = GUI_CONFIG["window_title"]
GUI_MIN_WIDTH = GUI_CONFIG["min_width"]
GUI_MIN_HEIGHT = GUI_CONFIG["min_height"]
GUI_DEFAULT_TEXT = GUI_CONFIG["default_text"]
GUI_SPLITTER_SIZES = GUI_CONFIG["splitter_sizes"]
GUI_COLORS = GUI_CONFIG["colors"]

MODIFICATION_ERROR_HINT = ", ".join(MODIFICATION_TYPES)


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


@dataclass(frozen=True)
class AvalancheQuality:
    """Текстовая оценка качества лавинного эффекта."""
    level: str
    title: str
    description: str


def compute_hash(text: str, algorithm: str = DEFAULT_ALGORITHM) -> str:
    """Вычислить хеш строки."""
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Неподдерживаемый алгоритм '{algorithm}'. "
            f"Доступны: {', '.join(SUPPORTED_ALGORITHMS)}"
        )
    h = hashlib.new(algorithm, text.encode(TEXT_ENCODING))
    return h.hexdigest()


def hash_to_bits(hex_digest: str) -> str:
    """Преобразовать hex-хеш в двоичную строку."""
    return bin(int(hex_digest, 16))[2:].zfill(len(hex_digest) * BITS_IN_HEX_DIGIT)


def count_differing_bits(hash1: str, hash2: str) -> int:
    """Подсчитать количество различающихся бит."""
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
    """Заменить один символ на другой."""
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


def change_one_bit(
    text: str,
    byte_index: int | None = None,
    bit_index: int | None = None,
) -> tuple[str, int, int]:
    """Инвертировать один бит в байтовом представлении строки."""
    if not text:
        raise ValueError("Строка не должна быть пустой.")
    data = bytearray(text.encode(TEXT_ENCODING))
    if byte_index is None:
        byte_index = random.randint(0, len(data) - 1)
    byte_index = byte_index % len(data)
    if bit_index is None:
        bit_index = random.randint(0, BITS_IN_BYTE - 1)
    bit_index = bit_index % BITS_IN_BYTE
    data[byte_index] ^= (1 << bit_index)
    try:
        modified = data.decode(TEXT_ENCODING)
    except UnicodeDecodeError:
        modified = data.decode(TEXT_ENCODING, errors=DECODE_ERRORS)
    return modified, byte_index, bit_index


def change_case(text: str, position: int | None = None) -> tuple[str, int]:
    """Изменить регистр одной буквы."""
    letter_positions = [i for i, c in enumerate(text) if c.isalpha()]
    if not letter_positions:
        raise ValueError("В строке нет букв для изменения регистра.")
    if position is None or position not in letter_positions:
        position = random.choice(letter_positions)
    char = text[position]
    new_char = char.lower() if char.isupper() else char.upper()
    modified = text[:position] + new_char + text[position + 1:]
    return modified, position


def format_modification_error(modification: str) -> str:
    return (
        f"Неизвестный тип модификации: '{modification}'. "
        f"Ожидается: {MODIFICATION_ERROR_HINT}."
    )


def get_avalanche_quality(percent: float) -> AvalancheQuality:
    """Вернуть оценку качества лавинного эффекта по проценту различий."""
    match percent:
        case p if p >= EXCELLENT_AVALANCHE_PERCENT:
            level = "excellent"
        case p if p >= MODERATE_AVALANCHE_PERCENT:
            level = "moderate"
        case _:
            level = "weak"

    level_config = QUALITY_LEVELS[level]
    return AvalancheQuality(
        level=level,
        title=level_config["title"],
        description=level_config["description"],
    )


def run_single_experiment(
    original: str,
    modification: str = "char",
    algorithm: str = DEFAULT_ALGORITHM,
) -> AvalancheResult:
    """Провести один эксперимент лавинного эффекта."""
    match modification:
        case "char":
            modified, _ = change_one_char(original)
            mod_label = MODIFICATION_LABELS["char"]
        case "bit":
            modified, byte_i, bit_i = change_one_bit(original)
            mod_label = MODIFICATION_LABELS["bit"].format(byte_i=byte_i, bit_i=bit_i)
        case "case":
            modified, pos = change_case(original)
            mod_label = MODIFICATION_LABELS["case"].format(pos=pos)
        case _:
            raise ValueError(format_modification_error(modification))

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
    count: int = DEFAULT_EXPERIMENT_COUNT,
    algorithm: str = DEFAULT_ALGORITHM,
    progress_callback=None,
) -> list[AvalancheResult]:
    """Провести серию экспериментов по всем типам модификаций."""
    if count < MIN_EXPERIMENT_COUNT:
        raise ValueError(f"Количество экспериментов должно быть >= {MIN_EXPERIMENT_COUNT}.")
    results = []
    total_steps = count * len(MODIFICATION_TYPES)
    step = 0
    for mod in MODIFICATION_TYPES:
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
    """Сводная статистика по списку результатов."""
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
        "total_bits": results[0].total_bits,
        "by_modification": {
            mod: round(sum(vals) / len(vals), 2)
            for mod, vals in by_mod.items()
        },
    }

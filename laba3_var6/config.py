import json
from pathlib import Path
from exceptions import ConfigError


class ConfigLoader:
    DEFAULT_CONFIG = "settings.json"

    REQUIRED_FIELDS = [
        'input_file', 'encrypted_file', 'decrypted_file',
        'encrypted_sym_key', 'public_key', 'private_key',
        'seed_block_bits', 'seed_key_bytes', 'seed_iv_bytes',
        'rsa_key_bits', 'rsa_exponent', 'text_encoding'
    ]

    def __init__(self, path: str = None):
        self.cfg_path = path or self.DEFAULT_CONFIG
        self._data = self._read_config()

    def _read_config(self) -> dict:
        try:
            with open(self.cfg_path, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
        except FileNotFoundError:
            raise ConfigError(f"Файл настроек '{self.cfg_path}' отсутствует")
        except json.JSONDecodeError as err:
            raise ConfigError(f"Ошибка парсинга JSON: {err}")

        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        if missing:
            raise ConfigError(f"Не хватает полей: {', '.join(missing)}")
        return data

    @property
    def input_path(self) -> str:
        return self._data['input_file']

    @property
    def encrypted_path(self) -> str:
        return self._data['encrypted_file']

    @property
    def decrypted_path(self) -> str:
        return self._data['decrypted_file']

    @property
    def sym_enc_path(self) -> str:
        return self._data['encrypted_sym_key']

    @property
    def public_path(self) -> str:
        return self._data['public_key']

    @property
    def private_path(self) -> str:
        return self._data['private_key']

    @property
    def seed_block_bits(self) -> int:
        return self._data['seed_block_bits']

    @property
    def seed_key_len(self) -> int:
        return self._data['seed_key_bytes']

    @property
    def seed_iv_len(self) -> int:
        return self._data['seed_iv_bytes']

    @property
    def rsa_bits(self) -> int:
        return self._data['rsa_key_bits']

    @property
    def rsa_exp(self) -> int:
        return self._data['rsa_exponent']

    @property
    def encoding(self) -> str:
        return self._data['text_encoding']

    def prepare_folders(self):
        paths = ['input_file', 'encrypted_file', 'decrypted_file',
                 'encrypted_sym_key', 'public_key', 'private_key']
        for key in paths:
            Path(self._data[key]).parent.mkdir(parents=True, exist_ok=True)
class HybridSystemError(Exception):
    pass

class ConfigError(HybridSystemError):
    pass

class FileOperationError(HybridSystemError):
    pass

class KeyGenError(HybridSystemError):
    pass

class EncryptError(HybridSystemError):
    pass

class DecryptError(HybridSystemError):
    pass

class KeyLoadError(HybridSystemError):
    pass
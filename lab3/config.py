"""
Configuration module for hybrid crypto system.

Contains all cryptographic constants and parameters used throughout the system,
including key sizes, block sizes, and algorithm-specific configurations.

Constants:
    SEED_KEY_SIZE: Size of SEED symmetric key in bytes (16 bytes = 128 bits)
    SEED_BLOCK_SIZE: SEED block size in bytes (16 bytes = 128 bits)
    RSA_KEY_SIZE: RSA key size in bits (2048 bits for security)
    PUBLIC_EXPONENT: RSA public exponent (65537 - standard secure value)
    IV_SIZE: Initialization Vector size for CBC mode in bytes (16 bytes = 128 bits)
"""

SEED_KEY_SIZE = 16
SEED_BLOCK_SIZE = 128
RSA_KEY_SIZE = 2048
PUBLIC_EXPONENT = 65537
IV_SIZE = 16
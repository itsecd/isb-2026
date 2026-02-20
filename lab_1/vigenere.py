#!/usr/bin/env python3

def encrypt_vigenere(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext += encrypted_char
            key_index += 1
        else:
            ciphertext += char
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            plaintext += decrypted_char
            key_index += 1
        else:
            plaintext += char
    return plaintext

def main():
    pass

if __name__ == "__main__":
    main()
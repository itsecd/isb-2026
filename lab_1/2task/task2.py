import json
import os
import argparse

import constants


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="cod5.txt")
    parser.add_argument("-k1", "--key1", default="key_1.json")
    parser.add_argument("-k2", "--key2", default="key_2.json")
    parser.add_argument("-o1", "--output1", default="decrypted_1.txt")
    parser.add_argument("-o2", "--output2", default="decrypted_2.txt")
    parser.add_argument("-ef", "--encrypted-freq", default="freq_encrypted.json")
    return parser.parse_args()


def read_file(filename, json_file=False):
    try:
        f = open(filename, "r", encoding="utf-8")
        if json_file:
            data = json.load(f)
        else:
            data = f.read()
        f.close()
        return data
    except FileNotFoundError:
        if json_file:
            return None
        print("Файл не найден!")
        return None


def write_file(data, filename, json_file=False):
    f = open(filename, "w", encoding="utf-8")
    if json_file:
        json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        f.write(data)
    f.close()
    print("Сохранено:", filename)


def count_freq(text):
    freq = {}
    total = len(text)
    if total == 0:
        return freq
    
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    for char in freq:
        freq[char] = freq[char] / total

    sorted_freq = {}
    sorted_keys = sorted(freq, key=freq.get, reverse=True)
    for key in sorted_keys:
        sorted_freq[key] = freq[key]
    
    return sorted_freq


def make_key(encrypted_freq, sample_freq):
    key = {}
    enc_list = []
    samp_list = []
    
    for k in encrypted_freq:
        enc_list.append(k)
    for k in sample_freq:
        samp_list.append(k)
    
    for i in range(len(enc_list)):
        if i < len(samp_list):
            key[enc_list[i]] = samp_list[i]
        else:
            key[enc_list[i]] = enc_list[i]
    
    return key


def main():
    args = get_args()
    
    encrypted = read_file(args.input)
    if encrypted is None:
        return
    print("Текст загружен")
    
    print("Считаю частоты...")
    enc_freq = count_freq(encrypted)
    write_file(enc_freq, args.encrypted_freq, json_file=True)
    
    key1 = read_file(args.key1, json_file=True)
    if key1 is None:
        print("Делаю первый ключ...")
        key1 = make_key(enc_freq, constants.REFERENCE_FREQUENCIES)
        write_file(key1, args.key1, json_file=True)


if __name__ == "__main__":
    main()
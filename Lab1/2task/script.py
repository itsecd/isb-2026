import re

def intput_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(f"File {filename} ready to work")
            return file.read()
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""

def output_file(filename: str, text: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
        file.write("\n")

start_string = intput_file("text.txt")
alfa_text = intput_file("alfa.txt")


total = len(start_string)
freq_abs = {}
for ch in start_string:
    freq_abs[ch] = freq_abs.get(ch, 0) + 1
freq_percent = {ch: count / total for ch, count in freq_abs.items()}

def parse_alfa(text: str):
    pattern = r'([А-ЯЁ=])\s*=\s*([\d.]+)'
    matches = re.findall(pattern, text)
    return {(' ' if letter == '=' else letter): float(value) for letter, value in matches}
ref_freq = parse_alfa(alfa_text)
ref_freq[" "] = 0.128675
if '\n' in ref_freq:
    del ref_freq['\n']

sorted_ref = sorted(ref_freq.items(), key=lambda x: x[1], reverse=True)
sorted_text = sorted(freq_percent.items(), key=lambda x: x[1], reverse=True)

dictionary = []
for i in range(min(len(sorted_text), len(sorted_ref))):
    text_char, text_freq = sorted_text[i]
    ref_letter, ref_freq_val = sorted_ref[i]
    dictionary.append([ref_letter, text_char])

print("Словарь (буква -> символ):")
print(dictionary, "\n")

key_content = intput_file("key.txt").strip().splitlines()
replace_dict = {}
for line in key_content:
    if ':' in line:
        parts = line.split(':', 1)
        src_char = parts[0].strip()
        dst_char = parts[1]       
        if src_char:
            replace_dict[src_char] = dst_char

trans_table = str.maketrans(replace_dict)

decrypted_text = start_string.translate(trans_table)

print("Результат расшифровки:")
print(decrypted_text)

output_file("decrypted.txt", decrypted_text)
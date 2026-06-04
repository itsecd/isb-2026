import json
from collections import Counter

RUS_FREQ = {
    ' ': 0.128675, 'О': 0.096456, 'И': 0.075312, 'Е': 0.072292, 'А': 0.064841,
    'Н': 0.061820, 'Т': 0.061619, 'С': 0.051953, 'Р': 0.040677, 'В': 0.039267,
    'М': 0.029803, 'Л': 0.029400, 'Д': 0.026983, 'Я': 0.026379, 'К': 0.025977,
    'П': 0.024768, 'З': 0.015908, 'Ы': 0.015707, 'Ь': 0.015103, 'У': 0.013290,
    'Ч': 0.011679, 'Ж': 0.010673, 'Г': 0.009867, 'Х': 0.008659, 'Ф': 0.007249,
    'Й': 0.006847, 'Ю': 0.006847, 'Б': 0.006645, 'Ц': 0.005034, 'Ш': 0.004229,
    'Щ': 0.003625, 'Э': 0.002416, 'Ъ': 0.000000
}

RUS_LETTERS_LOWER = set("абвгдежзийклмнопрстуфхцчшщъыьэюя ")

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def save_text(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[OK] {filename}")

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[OK] {filename}")

def frequency_analysis_all(text):
    total = len(text)
    if total == 0:
        return {}
    counter = Counter(text)
    return {ch: count/total for ch, count in counter.items()}

def get_freq_lines(ciphertext, top_n=30):
    freq = frequency_analysis_all(ciphertext)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [f"{display_char(ch)} : {f:.6f}" for ch, f in sorted_freq]

def get_rus_freq_lines(top_n=30):
    sorted_rus = sorted(RUS_FREQ.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [f"{display_char(ch)} : {f:.6f}" for ch, f in sorted_rus]

def get_mapping_lines(subst_map):
    items = []
    for sym in sorted(subst_map.keys()):
        mapped = subst_map[sym]
        if mapped is None:
            items.append(f"{display_char(sym)} : ")
        else:
            items.append(f"{display_char(sym)} -> {mapped}")
    return items

def display_char(ch):
    return '_' if ch == ' ' else ch

def apply_substitutions(text, subst_map):
    result = []
    for ch in text:
        if ch in subst_map and subst_map[ch] is not None:
            result.append(subst_map[ch])
        else:
            result.append(ch)
    return ''.join(result)

def print_three_columns(col1, col2, col3, width1=38, width2=35, width3=30):
    max_len = max(len(col1), len(col2), len(col3))
    col1 += [''] * (max_len - len(col1))
    col2 += [''] * (max_len - len(col2))
    col3 += [''] * (max_len - len(col3))
    for l1, l2, l3 in zip(col1, col2, col3):
        print(f"{l1:<{width1}} | {l2:<{width2}} | {l3}")

def main():
    print("=== ИНТЕРАКТИВНОЕ РАСШИФРОВАНИЕ (ручная подстановка, строчные буквы) ===")
    ciphertext = load_text("task2_encrypted.txt")
    
    freq_all = frequency_analysis_all(ciphertext)
    save_json("freq_analysis.json", freq_all)
    
    all_symbols = sorted(set(ciphertext))
    subst_map = {sym: None for sym in all_symbols}
    
    while True:
        current_decrypted = apply_substitutions(ciphertext, subst_map)
        
        col1 = ["ЧАСТОТЫ ШИФРОТЕКСТА (все символы)"] + get_freq_lines(ciphertext)
        col2 = ["ЭТАЛОННЫЕ ЧАСТОТЫ"] + get_rus_freq_lines()
        col3 = ["ТАБЛИЦА ЗАМЕН"] + get_mapping_lines(subst_map)
        
        print("\n" + "="*110)
        print_three_columns(col1, col2, col3, width1=38, width2=35, width3=30)
        print("="*110)
        
        print("\n=== РАСШИФРОВАННЫЙ ТЕКСТ (весь) ===")
        print(current_decrypted)
        print("="*110)
        
        cmd = input("\n> Введите команду (символ=буква / show / save / exit): ").strip()
        if cmd.lower() == "exit":
            break
        elif cmd.lower() == "show":
            continue
        elif cmd.lower() == "save":
            save_text("task2_decrypted.txt", current_decrypted)
            reverse_key = {}
            for sym, plain in subst_map.items():
                if plain is not None:
                    reverse_key[plain] = sym
            for ch in "абвгдежзийклмнопрстуфхцчшщъыьэюя ":
                if ch not in reverse_key:
                    reverse_key[ch] = ch
            save_json("task2_key.json", reverse_key)
            save_json("freq_analysis.json", freq_all)
            continue
        
        if "=" not in cmd:
            print("Неверный формат. Используйте: символ=буква (например, Х=о или _= )")
            continue
        
        sym, rus = cmd.split("=", 1)
        sym = sym.strip()
        rus = rus.strip()
        if sym == '_':
            sym = ' '
        if rus == '_':
            rus = ' '
        
        if len(sym) != 1:
            print("Слева должен быть ровно один символ")
            continue
        if rus and len(rus) != 1:
            print("Справа должна быть одна русская буква или пробел")
            continue
        
        if rus:
            rus_lower = rus.lower()
            if rus_lower not in RUS_LETTERS_LOWER:
                print("Недопустимая русская буква. Используйте буквы от а до я или _ для пробела.")
                continue
            rus = rus_lower
        
        if rus == "":
            subst_map[sym] = None
            print(f"[OK] Символ '{display_char(sym)}' больше не заменяется")
        else:
            subst_map[sym] = rus
            print(f"[OK] {display_char(sym)} -> {rus}")
    
    ans = input("\nСохранить результаты перед выходом? (y/n): ").strip().lower()
    if ans == 'y':
        final_decrypted = apply_substitutions(ciphertext, subst_map)
        save_text("task2_decrypted.txt", final_decrypted)
        reverse_key = {}
        for sym, plain in subst_map.items():
            if plain is not None:
                reverse_key[plain] = sym
        for ch in "абвгдежзийклмнопрстуфхцчшщъыьэюя ":
            if ch not in reverse_key:
                reverse_key[ch] = ch
        save_json("task2_key.json", reverse_key)
        save_json("freq_analysis.json", freq_all)
        print("Сохранено.")
    print("До свидания!")

if __name__ == "__main__":
    main()
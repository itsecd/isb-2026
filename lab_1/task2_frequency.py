from collections import Counter
from datetime import datetime

class FrequencyAnalyzer:
    def __init__(self):
        # Точные частоты русского языка
        self.russian = {
            ' ': 0.128675, 'о': 0.096456, 'и': 0.075312, 'е': 0.072292,
            'а': 0.064841, 'н': 0.061820, 'т': 0.061619, 'с': 0.051953,
            'р': 0.040677, 'в': 0.039267, 'м': 0.029803, 'л': 0.029400,
            'д': 0.026983, 'я': 0.026379, 'к': 0.025977, 'п': 0.024768,
            'з': 0.015908, 'ы': 0.015707, 'ь': 0.015103, 'у': 0.013290,
            'ч': 0.011679, 'ж': 0.010673, 'г': 0.009867, 'х': 0.008659,
            'ф': 0.007249, 'й': 0.006847, 'ю': 0.006847, 'б': 0.006645,
            'ц': 0.005034, 'ш': 0.004229, 'щ': 0.003625, 'э': 0.002416,
            'ъ': 0.000000
        }
        # Цвета
        self.GREEN = '\033[92m'
        self.BOLD = '\033[1m'
        self.END = '\033[0m'
    
    def get_freq(self, text):
        # Чистим от переносов строк
        clean = text.lower().replace('\n', '').replace('\r', '')
        total = len(clean)
        if total == 0:
            return {}, {}, 0
        counter = Counter(clean)
        freq = {c: count/total for c, count in counter.items()}
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)), counter, total
    
    def print_freq(self, enc_freq, enc_counter, total):
        print("\n" + "="*100)
        print("ЧАСТОТЫ СИМВОЛОВ")
        print("="*100)
        print(" №  |  Символ (текст)  |   Частота %   | Кол-во | Символ (рус) | Частота % ")
        print("-"*100)
        
        enc_items = list(enc_freq.items())
        rus_items = list(self.russian.items())
        
        for i in range(max(len(enc_items), len(rus_items))):
            # Текст
            if i < len(enc_items):
                ec, ef = enc_items[i]
                e_disp = repr(ec) if ec == ' ' else ec
                e_perc = ef * 100
                e_cnt = enc_counter[ec]
                e_str = f"'{e_disp}'"
            else:
                e_str, e_perc, e_cnt = "-", 0, 0
            
            # Русский
            if i < len(rus_items):
                rc, rf = rus_items[i]
                r_disp = repr(rc) if rc == ' ' else rc
                r_perc = rf * 100
                r_str = f"'{r_disp}'"
            else:
                r_str, r_perc = "-", 0
            
            print(f" {i+1:2} |     {e_str:6}     |    {e_perc:6.2f}    |  {e_cnt:3}   |    {r_str:6}    |   {r_perc:6.2f}")
    
    def decrypt(self, text, subs):
        colored, plain = [], []
        for ch in text:
            if ch in '\n\r':
                colored.append(ch)
                plain.append(ch)
                continue
            ch_low = ch.lower()
            if ch_low in subs:
                new = subs[ch_low].upper() if ch.isupper() else subs[ch_low]
                colored.append(f"{self.GREEN}{self.BOLD}{new}{self.END}")
                plain.append(new)
            else:
                colored.append(ch)
                plain.append(ch)
        return ''.join(colored), ''.join(plain)
    
    def save(self, text, subs, variant):
        _, plain = self.decrypt(text, subs)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Текст
        txt_file = f"task2_decoded_var{variant}_{ts}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(plain)
        print(f"\n✓ Результат: {txt_file}")
        
        # Ключ
        key_file = f"task2_key_var{variant}_{ts}.txt"
        with open(key_file, 'w', encoding='utf-8') as f:
            f.write("ЗАМЕНЫ:\n")
            for k, v in sorted(subs.items()):
                vv = '_' if v == ' ' else v
                f.write(f"'{k}' -> '{vv}'\n")
        print(f"✓ Ключ: {key_file}")
    
    def interactive(self, text, variant):
        subs = {}
        history = []
        freq, cnt, total = self.get_freq(text)
        
        print("\n" + "="*100)
        print("РЕЖИМ ЗАМЕН")
        print("="*100)
        print("Команды: x->y, x->_, show, freq, list, undo, reset, save, done")
        
        self.print_freq(freq, cnt, total)
        
        while True:
            colored, _ = self.decrypt(text, subs)
            print("\n" + "="*100)
            print("РЕЗУЛЬТАТ (зеленым - заменено):")
            print("-"*100)
            print(colored)
            if subs:
                print("\nЗамены:", ", ".join([f"{k}->{'_' if v==' ' else v}" for k,v in subs.items()]))
            print("="*100)
            
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'done':
                self.save(text, subs, variant)
                break
            elif cmd == 'freq':
                freq, cnt, total = self.get_freq(text)
                self.print_freq(freq, cnt, total)
            elif cmd == 'list':
                for k,v in sorted(subs.items()):
                    print(f"  '{k}' -> '{'_' if v==' ' else v}'")
            elif cmd == 'undo' and history:
                del subs[history.pop()]
                print("Отмена")
            elif cmd == 'reset':
                subs = {}
                history = []
                print("Сброс")
            elif '->' in cmd:
                parts = cmd.split('->')
                if len(parts) == 2:
                    frm = parts[0].strip()
                    to = parts[1].strip()
                    if len(frm) == 1:
                        if to == '_':
                            to = ' '
                        subs[frm] = to
                        history.append(frm)
                        print(f"Добавлено: '{frm}' -> '{'_' if to==' ' else to}'")
                    else:
                        print("Ошибка: нужен один символ")

def run():
    print("\n" + "="*80)
    print("ЗАДАНИЕ 2: Частотный анализ (вариант 11)")
    print("="*80)
    
    try:
        with open('code11.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        print("Загружен code11.txt")
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return
    
    with open('task2_encrypted_var11.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Сохранено в task2_encrypted_var11.txt")
    
    print("\nТЕКСТ:")
    print("-"*50)
    print(text)
    
    analyzer = FrequencyAnalyzer()
    analyzer.interactive(text, "11")
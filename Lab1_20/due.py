from __future__ import annotations
from collections import Counter
from pathlib import Path
from typing import Dict

def load_data(file: str | Path, strip_nl: bool = True) -> str:
    """Загружаем текст из файла."""
    text = Path(file).read_text(encoding="utf-8")
    return text.replace("\n", "") if strip_nl else text

def get_stats(text: str, limit: int | None = 10) -> tuple[Counter, str]:
    """Анализ частоты символов."""
    cnt = Counter(text)
    total = sum(cnt.values())
    top = cnt.most_common() if limit is None else cnt.most_common(limit)
    
    lines = ["Статистика встречаемости символов:", "-" * 45,
             f"{'Символ':<10} {'Кол-во':<12} {'Частота':<15}", "-" * 45]
    
    for ch, occ in top:
        lines.append(f"{repr(ch):<10} {occ:<12} {(occ/total):>10.4f}" if total else "")
    
    lines.extend(["-" * 55, f"Всего символов: {total}"])
    return cnt, "\n".join(lines)

def save_stats(data: Counter, path: str | Path, summary: bool = True, percent: bool = True) -> None:
    """Сохраняем статистику в файл."""
    total = sum(data.values())
    lines = ["Результаты анализа частоты символов", "=" * 65,
             f"{'Символ':<15} {'Кол-во':<12}" + (f"{'Частота':<15}" if percent else ""),
             "-" * 65]
    
    for ch, freq in data.most_common():
        if percent:
            pct = (freq / total)  if total else 0
            lines.append(f"{repr(ch):<15} {freq:<12} {pct:>12.4f}")
        else:
            lines.append(f"{repr(ch):<15} {freq:<12}")
    
    if summary:
        lines.extend(["-" * 55, f"{'ВСЕГО':<15} {total:<12}", f"{'УНИКАЛЬНЫХ':<15} {len(data):<12}"])
    
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

def substitute(text: str, rules: Dict[str, str]) -> str:
    """Заменяеv символы по правилам."""
    if any(len(k) != 1 or len(v) != 1 for k, v in rules.items()):
        raise ValueError("Правила должны быть одиночными символами")
    for s, t in rules.items():
        text = text.replace(s, t)
    return text

def interactive(text: str) -> None:
    """Табличка для ввода команд."""
    print(f"\n=== РАСШИФРОВКА ===\n{text[:500]}{'...' if len(text)>500 else ''}")
    rules = {}
    
    while True:
        print("\n" + "="*50 + "\nТекущие подстановки:")
        [print(f"  '{k}' -> '{v}'") for k, v in rules.items()] or print("  Нет правил")
        
        cmd = input("\n1:Добавить правило замены\n2:Показать текст \n3:Сброс правил замены \n4:Сохранить в файл \n5:Статистика символов \n6:Выход\n> ").strip()
        
        if cmd == "1":
            s, t = input("Заменить: "), input("На: ")
            if len(s) == 1 and len(t) == 1:

                rules[s] = t
                print(f"Добавлено: '{s}' -> '{t}'")
            else:
                print("Ошибка: нужен 1 символ")
        
        elif cmd == "2" and rules:
            res = substitute(text, rules)
            print(f"\n{'='*50}\nРЕЗУЛЬТАТ:\n{'='*50}\n{res[:1000]}{'...' if len(res)>1000 else ''}")
        
        elif cmd == "3":
            rules.clear()
            print("Правила сброшены")
        
        elif cmd == "4" and rules:
            name = input("Имя файла: ").strip() or "out.txt"
            Path(name).write_text(substitute(text, rules), encoding="utf-8")
            print(f"Сохранено в {name}")
        
        elif cmd == "5":
            print(get_stats(text, 20)[1])
        
        elif cmd == "6":
            print("Выход")
            break
        else:
            print("Неверный ввод")

def main() -> None:
    """мэйн."""
    src = input("Файл с текстом: ").strip() or "encrypted.txt"
    
    try:
        data = load_data(src)
    except FileNotFoundError:
        print(f"Файл {src} не найден")
        return
    
    stats, report = get_stats(data)
    print(report)
    
    out = input("\nСохранить статистику: ").strip() or "symbol_stats.txt"
    save_stats(stats, out)
    print(f"Статистика сохранена в {out}")
    interactive(data)

if __name__ == "__main__":
    main()
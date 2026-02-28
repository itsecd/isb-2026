import os
import argparse

from nist_io import read_bitstring, ensure_dir, write_text
from nist_monobit import monobit_test
from nist_runs import runs_test
from nist_longest_run import longest_run_in_block_prepare, parse_p_value


def main() -> None:
    """Запускает 3 теста NIST для 128-битной последовательности и сохраняет результаты в файлы."""
    parser = argparse.ArgumentParser(
        description="3 теста NIST для бинарной последовательности длиной 128 бит."
    )
    parser.add_argument("seq_file", help="Файл с 128-битной строкой из 0/1")
    parser.add_argument("out_dir", help="Папка для результатов (будет создана при необходимости)")
    parser.add_argument("--alpha", type=float, default=0.01, help="Уровень значимости (по умолчанию 0.01)")
    args = parser.parse_args()

    print("=== NIST-тесты для последовательности 128 бит ===")
    print(f"Последовательность читается из файла: {args.seq_file}")

    ensure_dir(args.out_dir)
    seq: str = read_bitstring(args.seq_file, expected_len=128)

    # Monobit
    print("\n[1/3] Частотный побитовый тест...")
    s, p_mono = monobit_test(seq)
    mono_pass: bool = (p_mono >= args.alpha)

    mono_text: str = (
        "NIST Частотный побитовый тест\n"
        f"Файл: {args.seq_file}\n"
        f"N = {len(seq)}\n"
        f"S = Σ x_i = {s}\n"
        f"P-value = erfc(|S|/sqrt(2N)) = {p_mono:.10f}\n"
        f"Решение (alpha={args.alpha}): {'ПРОЙДЕН' if mono_pass else 'НЕ ПРОЙДЕН'}\n"
    )
    write_text(os.path.join(args.out_dir, "monobit_result.txt"), mono_text)
    print(f"Готово. P-value = {p_mono:.6f}. Файл: {os.path.join(args.out_dir, 'monobit_result.txt')}")

    # Runs
    print("\n[2/3] Тест на одинаковые подряд идущие биты...")
    pi, vn, p_runs, condition_ok = runs_test(seq)
    runs_pass: bool = (p_runs >= args.alpha)

    runs_text: str = (
        "NIST Тест на одинаковые подряд идущие биты\n"
        f"Файл: {args.seq_file}\n"
        f"N = {len(seq)}\n"
        f"pi = (#единиц)/N = {pi:.10f}\n"
    )
    if not condition_ok:
        runs_text += (
            "Условие не выполнено: |pi - 1/2| >= 2/sqrt(N)\n"
            "P-value = 0\n"
            f"Решение (alpha={args.alpha}): НЕ ПРОЙДЕН\n"
        )
        print("Условие не выполнено, P-value = 0.000000.")
    else:
        runs_text += (
            f"Vn = 1 + #(ε_i != ε_(i+1)) = {vn}\n"
            f"P-value = erfc(|Vn - 2Npi(1-pi)| / (2*sqrt(2N)*pi(1-pi))) = {p_runs:.10f}\n"
            f"Решение (alpha={args.alpha}): {'ПРОЙДЕН' if runs_pass else 'НЕ ПРОЙДЕН'}\n"
        )
        print(f"Готово. P-value = {p_runs:.6f}.")
    write_text(os.path.join(args.out_dir, "runs_result.txt"), runs_text)
    print(f"Файл: {os.path.join(args.out_dir, 'runs_result.txt')}")

    # Longest Run
    print("\n[3/3] Тест на самую длинную последовательность единиц в блоке...")
    v, chi2, k, a, x = longest_run_in_block_prepare(seq)

    print("Для онлайн-калькулятора неполной гамма-функции нужны параметры:")
    print(f"  a = K/2 = {a:.10f}")
    print(f"  x = chi^2/2 = {x:.10f}")
    print("Вставьте посчитанный P-value (igamc(a, x)).")

    while True:
        try:
            p_in: str = input("Введите значение P-value (0..1): ")
            p_long: float = parse_p_value(p_in)
            break
        except Exception as e:
            print(f"Ошибка ввода: {e}. Попробуйте ещё раз.")

    long_pass: bool = (p_long >= args.alpha)

    long_text: str = (
        "NIST Тест на самую длинную последовательность единиц в блоке (N=128, M=8)\n"
        f"Файл: {args.seq_file}\n"
        f"N = {len(seq)}, M = 8, блоков = 16\n"
        "Категории:\n"
        "  v1: максимум <= 1\n"
        "  v2: максимум = 2\n"
        "  v3: максимум = 3\n"
        "  v4: максимум >= 4\n"
        f"Наблюдаемые v = [{v[0]}, {v[1]}, {v[2]}, {v[3]}]\n"
        "Теоретические pi (M=8): [0.2148, 0.3672, 0.2305, 0.1875]\n"
        f"χ^2 = {chi2:.10f}\n"
        f"K = {k}\n"
        f"a = K/2 = {a:.10f}\n"
        f"x = χ^2/2 = {x:.10f}\n"
        f"P-value (введено пользователем) = {p_long:.10f}\n"
        f"Решение (alpha={args.alpha}): {'ПРОЙДЕН' if long_pass else 'НЕ ПРОЙДЕН'}\n"
    )
    write_text(os.path.join(args.out_dir, "longest_run_result.txt"), long_text)
    print(f"Готово. P-value = {p_long:.6f}. Файл: {os.path.join(args.out_dir, 'longest_run_result.txt')}")

    # Итоговый результат
    summary: str = (
        f"Файл последовательности: {args.seq_file}\n"
        f"Папка результатов: {args.out_dir}\n"
        f"alpha = {args.alpha}\n\n"
        f"Частотный побитовый тест:  P={p_mono:.10f}  -> {'ПРОЙДЕН' if mono_pass else 'НЕ ПРОЙДЕН'}\n"
        f"Тест на одинаковые подряд идущие биты:     P={p_runs:.10f}  -> {'ПРОЙДЕН' if runs_pass else 'НЕ ПРОЙДЕН'}\n"
        f"Тест на самую длинную последовательность единиц в блоке:  P={p_long:.10f}  -> {'ПРОЙДЕН' if long_pass else 'НЕ ПРОЙДЕН'}\n\n"
        f"Итоговый вывод: {'ГПСЧ прошёл проверку' if long_pass and mono_pass and runs_pass else 'ГПСЧ не прошёл проверку одного или нескольких тестов'}\n"
    )
    write_text(os.path.join(args.out_dir, "выводы.txt"), summary)
    print(f"\nСводка сохранена в файл: {os.path.join(args.out_dir, 'выводы.txt')}")
    print("Работа завершена.")


if __name__ == "__main__":
    main()
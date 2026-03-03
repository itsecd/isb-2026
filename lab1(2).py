cipher_text = """Y8S-tA-!AYQSYxS3dAGYSRJ-=A-SUYItLJ-K-ARxOR$JQRALOZYI-JtAJYA$QJFAGYQO$8YxLJ$OFSYQJFA8$=QJx-=A8ORAI$E$S-RA!L8LnACUU$KJ-xS3$ALOZYI-Jt3AGYtYZLBJAYGJ-t-!-
IYxLJFAILhYJWAGIYZILttA-AQ-QJ$tAnJYAYQYh$SSYALKJWLOFSYAxACGYdWAhYOFEdA8LSS3d
GIYZILtt-IYxLS-
$AxAQxYBAYn$I$8FAGY!xYOR$JAQY!8LxLJFAGI-OYM$S-RA-AQ-QJ$t3AKYJYI3$ALxJYtLJ-!-IWBJAIWJ-SS3$A!L8Ln-AYh$QG$nxLRAW8YhQJxYA-AQKYIYQJFAx3GYOS$S-RAYG$IL>-=
QAIL!x-J-$tAJ$dSYOYZ-=AJLK-dAKLKA-QKWQQJx$SS3=A-SJ$OO$KJA-AtLE-SSY$AYhWn$S-$A-SUYItLJ-KLAQJLSYxJQRA$9$AhYO$$AxLMSY=
CJ-ASLGILxO$S-RAYJKI3xLBJASYx3$AZYI-!YSJ3AxALSLO-
!$A8LSS3dAGI$8QKL!LJ$OFSY=ALSLO-J-K$A-ALxJYtLJ-!L>--
AGIY>$QQYx
xLMSYAYJt$J-JFAnJYA-SUYItLJ-KLAS$AJYOFKYAQGYQYhQJxW$JAIL!x-J-BAJ$dSYOYZ-=ASYA-AUYIt-IW$JASYx3$AGY8dY83AKAI$E$S-BAQY>-
LOFS3dACKYSYt-n$QK-dA-ACKYOYZ-n$QKdAGIYhO$tA8$OLRAt-IAhYO$$A-ACUU$KJ-xS3t"""
chars = list(cipher_text)
total = len(chars)

freq = {}
for c in chars:
    freq[c] = freq.get(c, 0) + 1

sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)


print("ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА")
print(f"Всего символов: {total}")
print("\nСимвол | Кол-во | Частота")
print("-" * 30)
for c, count in sorted_freq:
    print(f"{c:6} | {count:6} | {count/total:.4f}")
print()

cipher = cipher_text

text = cipher.replace('A', ' ')          # Пробел
text = text.replace('Y', 'О')
text = text.replace('t', 'М')
text = text.replace('-', 'И')
text = text.replace('S', 'Н')
text = text.replace('J', 'Т')
text = text.replace('E', 'Ш')
text = text.replace('$', 'Е')           
text = text.replace('F', 'Ь')
text = text.replace('U', 'Ф')
text = text.replace('I', 'Р')
text = text.replace('L', 'А')
text = text.replace('C', 'Э')
text = text.replace('Q', 'С')
text = text.replace('O', 'Л')
text = text.replace('x', 'В')
text = text.replace('M', 'Ж')
text = text.replace('n', 'Ч')
text = text.replace('8', 'Д')
text = text.replace('!', 'З')
text = text.replace('G', 'П')
text = text.replace('W', 'У')
text = text.replace('d', 'Х')
text = text.replace('Z', 'Г')
text = text.replace('=', 'Й')
text = text.replace('3', 'Ы')
text = text.replace('h', 'Б')
text = text.replace('R', 'Я')
text = text.replace('>', 'Ц')
text = text.replace('B', 'Ю')
text = text.replace('9', 'Щ')

with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

key_mapping = {
    'A': ' ', 'Y': 'О', 't': 'М', '-': 'И', 'S': 'Н', 'J': 'Т', 'E': 'Ш',
    '$': 'Е', 'F': 'Ь', 'U': 'Ф', 'I': 'Р', 'L': 'А', 'C': 'Э', 'Q': 'С',
    'O': 'Л', 'x': 'В', 'M': 'Ж', 'n': 'Ч', '8': 'Д', '!': 'З', 'G': 'П',
    'W': 'У', 'd': 'Х', 'Z': 'Г', '=': 'Й', '3': 'Ы', 'h': 'Б', 'R': 'Я',
    '>': 'Ц', 'B': 'Ю', '9': 'Щ', 'K':'K'
}

with open('cipher_key.txt', 'w', encoding='utf-8') as f:
    f.write("КЛЮЧ ШИФРОВАНИЯ\n")
    f.write("Символ шифротекста -> Буква открытого текста\n")
    f.write("-" * 50 + "\n")
    for cipher_char in sorted(key_mapping.keys()):
        plain_char = key_mapping[cipher_char]
        f.write(f"'{cipher_char}' -> '{plain_char}'\n")

print("Дешифровка завершена. Файлы сохранены:")
print("decrypted_text.txt")
print("cipher_key.txt")

print(text)

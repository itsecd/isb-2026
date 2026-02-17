alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'

cipher_text = """!9$!KCMU9YIKMhLGYMhRG$9G$>ZPYdIZd!RMZP9$F$VC$!MIY-WhRMRM>IYIRCMhZ!Z9W$M!9$GLn!dCMdP$ARYVRd!LMPZMhRG$9G$>ZPYdIZd!RMFVCM>YJR!WMhRG$9P9Zd!9YId!-Y
FVCM>YJR!WMFYIIWQM-MhRG$9P9Zd!9YId!-$MdP$ARYVRd!YSMPZMhRG$9G$>ZPYdIZd!RMI$ZGQZFRSZMRdPZVK>Z-Y!KM9Y>IW$MIY-WhRMRM>IYIRCMRS$nJR$dCM-MRQM9YdPZ9CB$IRR
ZIRMFZVBIWMF$VY!KM3!ZMZd!Y-YCdKMIYMd!Z9ZI$M>YhZIY
hLGMhRG$9G$>ZPYdIZd!RM-WF$VC$!M!9RM-RFYMIY-WhZ-MRM>IYIRtMI$ZGQZFRSWQMFVCMZG$dP$O$IRCMFZVBIZUZML9Z-ICM>YJR!W
P$9-WtMIY-WhM-hVnOY$!M-Md$GCMRdPZVK>Z-YIR$M!$QIZVZURtMLd!9Ztd!-MRMP9ZFLh!Z-MFVCM>YJR!WMRIEZ9SYARZIIWQMdRd!$SMRMdF$9BR-YIRCMhRG$9P9$d!LPIRhZ-
dP$ARYVRd!WMPZMhRG$9G$>ZPYdIZd!RMR>-$d!IWMZ!VROIWSM-VYF$IR$SM!$QIRO$dhRSRMd9$Fd!-YSRMRS$nJRSRdCM-MRQM9YdPZ9CB$IRR
ZFIYhZMSYhhYSG$9MIYPZSRIY$!MRSMO!ZMZFIRQM!$QIRO$dhRQMd9$Fd!-MI$FZd!Y!ZOIZMO!ZGWMPZG$FR!KMhRG$9P9$d!LPIRhZ-
dP$ARYVRd!WMPZMhRG$9G$>ZPYdIZd!RMFZVBIWM!YhB$MPZd!9ZR!KMdRVKILnMZGZ9ZILMPL!$SMdZ>FYIRCMPZVR!RhMP9ZA$FL9MRM9$hZS$IFYARtMhZ!Z9W$MPZ>-ZVCn!MPZVK>Z-Y!$VCSMhRG$9P9Zd!9YId!-YMP9RS$IC!KM3EE$h!R-IW$MS$!ZFWM>YJR!WMRMZd!Y-Y!KdCM-MG$>ZPYdIZd!R
IYhZI$AMPZVK>Z-Y!$VRMhRG$9P9Zd!9YId!-YMFZVBIWMd!9$SR!KdCMGW!KMGZV$$MRIEZ9SR9Z-YIIWSRMZGMLU9Z>YQMhRG$9P9Zd!9YId!-YMRMEZ9SR9Z-Y!KMhLVK!L9LMhZ!Z9YCMPZ>-ZVC$!MLOR!KdCMRMPZVLOY!KMIZ-LnMRIEZ9SYARn"""

key = {
    'M': ' ',
    'I': 'Н', 
    'Y': 'А',
    'S': 'М',
    'Q': 'Х',
    'R': 'И',
    'Z': 'О',
    'E': 'Ф',
    '9': 'Р',
    'A': 'Ц',
    '-': 'В',
    'W': 'Ы',
    'h': 'К',
    '3': 'Э',
    '!': 'Т',
    '$': 'Е',
    'G': 'Б',
    'V': 'Л',
    'F': 'Д',
    'C': 'Я',
    '>': 'З',
    'P': 'П',
    'd': 'С',
    'L': 'У',
    'n': 'Ю',
    'J': 'Щ',
    't': 'Й',
    'U': 'Г',
    'K': 'Ь',
    'B': 'Ж',
    'O': 'Ч',
}

def decrypt(text, key):
    """Расшифровывает текст, заменяя символы по ключу"""
    result = []
    for line in text.split('\n'):
        decrypted_line = ''
        for char in line:
            if char in key:
                decrypted_line += key[char]
            else:
                decrypted_line += char
        decrypted_line += '. '
        result.append(decrypted_line)
    return ''.join(result)

decrypted_text = decrypt(cipher_text, key)

with open('task2_decryption.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted_text)

with open('task2_key.txt', 'w', encoding='utf-8') as f:
    f.write("КЛЮЧ ДЕШИФРОВКИ:\n")
    for k in sorted(key.keys()):
        if k == ' ':
            f.write(f"ПРОБЕЛ -> {key[k]}\n")
        else:
            f.write(f"{k} -> {key[k]}\n")

print("Дешифровка успешно выполнена")
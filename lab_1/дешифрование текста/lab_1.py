from collections import Counter


cipher_text = """!9$!KCMU9YIKMhLGYMhRG$9G$>ZPYdIZd!RMZP9$F$VC$!MIYWhRMRM>IYIRCMhZ!Z9W$M!9$GLn!dCMdP$ARYVRd!LMPZMhRG$9G$>
ZPYdIZd!RMFVCM>YJR!WMhRG$9P9Zd!9YId!-Y
FVCM>YJR!WMFYIIWQM-MhRG$9P9Zd!9YId!-
$MdP$ARYVRd!YSMPZMhRG$9G$>ZPYdIZd!RMI$ZGQZFRSZMRdPZVK>
Z-Y!KM9Y>IW$MIY-WhRMRM>IYIRCMRS$nJR$dCMMRQM9YdPZ9CB$IRR
ZIRMFZVBIWMF$VY!KM3!ZMZd!Y-YCdKMIYMd!Z9ZI$M>YhZIY
hLGMhRG$9G$>ZPYdIZd!RM-WF$VC$!M!9RM-RFYMIY-WhZMRM>IYIRtMI$ZGQZFRSWQMFVCMZG$dP$O$IRCMFZVBIZUZML9ZICM>YJR!W
P$9-WtMIY-WhM-hVnOY$!M-Md$GCMRdPZVK>ZYIR$M!$QIZVZURtMLd!9Ztd!-MRMP9ZFLh!ZMFVCM>YJR!WMRIEZ9SYARZIIWQMdRd!$SMRMdF$9BRYIRCMhRG$9P9$d!LPIRhZdP$ARYVRd!WMPZMhRG$9G$>ZPYdIZd!RMR>-$d!IWMZ!VROIWSMVYF$IR$SM!$QIRO$dhRSRMd9$Fd!-YSRMRS$nJRSRdCMMRQM9YdPZ9CB$IRR
ZFIYhZMSYhhYSG$9MIYPZSRIY$!MRSMO!ZMZFIRQM!$QIRO$dhRQMd9
$Fd!-MI$FZd!Y!ZOIZMO!ZGWMPZG$FR!KMhRG$9P9$d!LPIRhZdP$ARYVRd!WMPZMhRG$9G$>ZPYdIZd!RMFZVBIWM!YhB$MPZd!9ZR!
KMdRVKILnMZGZ9ZILMPL!$SMdZ>FYIRCMPZVR!RhMP9ZA$FL9MRM9
$hZS$IFYARtMhZ!Z9W$MPZ>-ZVCn!MPZVK>ZY!$VCSMhRG$9P9Zd!9YId!-YMP9RS$IC!KM3EE$h!RIW$MS$!ZFWM>YJR!WMRMZd!Y-Y!KdCM-MG$>ZPYdIZd!R
IYhZI$AMPZVK>Z-Y!$VRMhRG$9P9Zd!9YId!-
YMFZVBIWMd!9$SR!KdCMGW!KMGZV$$MRIEZ9SR9ZYIIWSRMZGMLU9Z>YQMhRG$9P9Zd!9YId!-YMRMEZ9SR9ZY!KMhLVK!L9LMhZ!Z9YCMPZ>-ZVC$!MLOR!KdCMRMPZVLOY!KMIZLnMRIEZ9SYARn"""


cipher_text = cipher_text.replace("\n", "")

#Частотный анализ
freq = Counter(cipher_text)
print("Частота символов (топ-10):")
for char, count in freq.most_common(10):
    print(f"'{char}': {count}")



def replace_symbol_in_text():

    print("=== ПРОГРАММА ЗАМЕНЫ СИМВОЛОВ ===")
    print(cipher_text)
    
    replacements = {}
    
    while True:
        print("\n" + "="*50)
        print("Текущие замены:")
        if replacements:
            for old, new in replacements.items():
                print(f"  '{old}' -> '{new}'")
        else:
            print("  Замен пока нет")
        
        print("\nВыберите действие:")
        print("1. Добавить/изменить замену")
        print("2. Показать текст с текущими заменами")
        print("3. Сбросить все замены")
        print("4. Сохранить результат в файл")
        print("5. Выйти")
        
        choice = input("\nВаш выбор (1-5): ").strip()
        
        if choice == '1':
            old_symbol = input("Введите символ, который нужно заменить: ")
            if len(old_symbol) != 1:
                print("Ошибка: введите один символ!")
                continue
            
            new_symbol = input("Введите символ для замены: ")
            if len(new_symbol) != 1:
                print("Ошибка: введите один символ!")
                continue
            
            replacements[old_symbol] = new_symbol
            print(f"Замена '{old_symbol}' -> '{new_symbol}' добавлена")
        
        elif choice == '2':
            if not replacements:
                print("Нет замен для применения!")
                continue
            
            modified_text = cipher_text
            for old, new in replacements.items():
                modified_text = modified_text.replace(old, new)
            
            print("\n" + "="*50)
            print("ТЕКСТ ПОСЛЕ ВСЕХ ЗАМЕН:")
            print("="*50)
            print(modified_text)
        
        elif choice == '3':
            replacements.clear()
            print("Все замены сброшены")
        
        elif choice == '4':
            if not replacements:
                print("Нет замен для сохранения!")
                continue
            
            modified_text = cipher_text
            for old, new in replacements.items():
                modified_text = modified_text.replace(old, new)
            
            filename = input("Введите имя файла для сохранения (по умолчанию: replaced_text.txt): ").strip()
            if not filename:
                filename = "replaced_text.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(modified_text)
            
            print(f"Текст сохранен в файл: {filename}")
        
        elif choice == '5':
            print("Программа завершена")
            break
        
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    replace_symbol_in_text()




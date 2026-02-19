def decrypt_text(encrypted_text, decryption_key):
    result = ""
    for char in encrypted_text:
        if char in decryption_key:
            result += decryption_key[char]
        else:
            result += char
    return result


if __name__ == "__main__":
    key = {
        "Y": " ",
        "Ё": "о",
        "К": "е",
        "Я": "и",
        "s": "л",
        "Й": "т",
        "U": "н",
        "Д": "к",
        "i": "ь",
        "ю": "р",
        "7": "п",
        "Q": "с",
        "И": "в",
        "R": "а",
        "г": "б",
        "@": "з",
        "Ж": "я",
        "О": "ш",
        "Т": "ж",
        "F": "э",
        "J": "й",
        "G": "ч",
        "Р": "ю",
        "1": "ы",
        "у": "ъ",
        "%": "д",
        "3": "м",
        "=": "г",
        "Z": "ц",
        "Х": "х",
        "N": "ф",
        "П": "щ",
        "<": "у",
    }
    encrypted_text = """7КUЙКQЙYЯsЯYЙКQЙЯюЁИRUЯКYURY7юЁUЯДUЁИКUЯКYЖИsЖКЙ
QЖYИRТUЁJYGRQЙiРYЁгКQ7КGКUЯЖYЯUNЁю3RZЯЁUUЁJYгК@Ё7RQUЁQЙЯ
FЙЁY3КЙЁ%YДЁЙЁю1JY7Ё@ИЁsЖКЙYИ1ЖИЯЙiY<Ж@ИЯ3ЁQЙЯYИY
ДЁ37iРЙКюU1ХYQЯQЙК3RХYQКЙЖХYЯYИКг7юЯsЁТКUЯЖХY7юКТ%
КYGК3YЯХYQ3Ё=<ЙYЯQ7Ёsi@ЁИRЙiY@sЁ<31ОsКUUЯДЯ
7юЁZКQQY7КUЙКQЙRYИДsРGRКЙYИYQКгЖYUКQДЁsiДЁYFЙR7ЁИY7
sRUЯюЁИRUЯКYQДRUЯюЁИRUЯКY7Ёs<GКUЯКY%ЁQЙ<7RY7Ё%%Кю
ТRUЯКY%ЁQЙ<7RYЯYRURsЯ@
URY7КюИЁ3YFЙR7КYQ7КZЯRsЯQЙ1YЁ7юК%КsЖРЙYЁгуК3YЙКQЙЯю
ЁИRUЯЖYИ1гЯюRЖYQЯQЙК31YЯY7юЯsЁТКUЯЖYДЁЙЁю1КYг<%<ЙY
7Ё%ИКю=RЙiQЖY7юЁИКюДК
@RЙК3YQY7Ё3ЁПiРYQ7КZЯRsЯ@ЯюЁИRUU1ХYЯUQЙю<3КUЙЁИY7ю
ЁИЁ%ЖЙQЖYQДRUЯюЁИRUЯЖY%sЖYИ1ЖИsКUЯЖY7ЁЙКUZЯRsiU1
ХY<Ж@ИЯ3ЁQЙКJ
URYFЙR7КY7Ёs<GКUЯЖY%ЁQЙ<7RY7КUЙКQЙКю1YЯQ7Ёsi@<РЙYюR
@sЯGU1КY3КЙЁ%1YЙRДЯКYДRДYFДQ7s<RЙRZЯЖY<Ж@ИЯ3ЁQЙКJY
ЯYQЁZЯRsiURЖYЯUТКUКюЯЖYGЙЁг1Y7юЁИКюЯЙiY3Ё=<ЙYsЯYЁUЯ
Y7Ёs<GЯЙiYUКQRUДZЯЁUЯюЁИRUU1JY%ЁQЙ<7YДYQЯQЙК3К
7ЁQsКY@RИКюОКUЯЖYЙКQЙЯюЁИRUЯЖYQЁQЙRИsЖКЙQЖYЁЙGК
ЙYИYДЁЙЁюЁ3YЁ7ЯQ1ИRРЙQЖYURJ%КUU1КY<Ж@ИЯ3ЁQЙЯYЯYюКДЁ3КU%R
ZЯЯY7ЁYЯХY<QЙюRUКUЯР
7КUЙКQЙYUКYЙЁsiДЁY7Ё3Ё=RКЙYИ1ЖИЯЙiYQsRг1КY3КQЙRYUЁYЯ
Y7ЁИ1ОRКЙYЁгПЯJY<юЁИКUiYгК@Ё7RQUЁQЙЯYЁю=RUЯ@RZЯЯY7Ё
@ИЁsЖЖY@RюRUККY7Ё%=ЁЙЁИЯЙiQЖYДYИЁ@3ЁТU13YRЙRДR3"""

    print("Расшифрованный текст:", decrypt_text(encrypted_text, key))

class DeFrequncy:
    def __init__(self, path_txt: str):

        ci_alph = {}

        text = ""
        with open(path_txt, 'r', encoding='utf-8') as file:
            text = file.read()

        for i in text:
            if i == '\n':
                ci_alph[' '] = ci_alph.get(' ', 0) + 1
            else:
                ci_alph[i] = ci_alph.get(i, 0) + 1
        ci_alph = dict(sorted(ci_alph.items(), key=lambda item: item[1], reverse=True))

        freq_alph = ""
        for i in ci_alph:
            freq_alph += i + ' | ' + str(ci_alph[i]) + '\n'

        with open("freq_alph.txt", 'w', encoding='utf-8') as file:
            file.write(freq_alph)

        alph_chance = [[' ', 0.128675], ['О', 0.096456], ['И', 0.075312],
                       ['Е', 0.072292], ['А', 0.064841], ['Н', 0.061820],
                       ['Т', 0.061619], ['С', 0.051953], ['Р', 0.040677],
                       ['В', 0.039267], ['М', 0.029803], ['Л', 0.029400],
                       ['Д', 0.026983], ['Я', 0.026379], ['К', 0.025977],
                       ['П', 0.024768], ['З', 0.015908], ['Ы', 0.015707],
                       ['Ь', 0.015103], ['У', 0.013290], ['Ч', 0.011679],
                       ['Ж', 0.010673], ['Г', 0.009867], ['Х', 0.008659],
                       ['Ф', 0.007249], ['Й', 0.006847], ['Ю', 0.006847],
                       ['Б', 0.006645], ['Ц', 0.005034], ['Ш', 0.004229],
                       ['Щ', 0.003625], ['Э', 0.002416], ['Ъ', 0.000000]]

        self.alph_key = [[],[]]

        j = 0
        for i in ci_alph:
            self.alph_key[0] += ([alph_chance[j][0]])
            self.alph_key[1] += ([i])
            j += 1

        self.de_text = ""
        for i in text:
            if i != '\n':
                self.de_text += self.alph_key[0][self.alph_key[1].index(i)]
            else:
                self.de_text += self.alph_key[0][self.alph_key[1].index(' ')]

    def key_to_text(self) -> str:
        """
        :return: строковое значение ключа
        """
        text = ""
        for i in range(33):
           text += "'" + self.alph_key[0][i] + "' | '" + self.alph_key[1][i] +  "'\n"
        return text

    def change_symbols(self, first: str, second: str) -> None:
        """
        :param first: первый символ для замены
        :param second: второй символ для замены
        :return: заменяет два символа местами в тексте и в ключе
        """
        first, second = first.upper(), second.upper()

        first_n = self.alph_key[0].index(first)
        second_n = self.alph_key[0].index(second)
        self.alph_key[0][first_n] = second
        self.alph_key[0][second_n] = first

        new_text = ""
        for i in self.de_text:
            j = ' '
            if i == first:
                j = second
            elif i == second:
                j = first
            else:
                j = i
            new_text += j
        self.de_text = new_text

decipher = DeFrequncy("cod2.txt")
while True:
    print("1 - output text")
    print("2 - output key")
    print("3 - output words of 1-2 symbols")
    print("4 - change symbols")
    print("5 - save key and deciphered text")
    print("6 - exit")
    a = input("input number of command: ")

    if a == '1':
        print(decipher.de_text)
    elif a == '2':
        text = decipher.key_to_text()
        print(text)
    elif a == '3':
        print("1 symbol: а, б, в, ж, и, к, о, с, у, я")
        print("2 symbols: на, не, по, до, от, за, ко, \n"
              "во, со, из, об, ад, за, он, мы, вы, ты, \n"
              "ее, их, ой, ай, ну, ох, ах, ел, ум, ус, ел")
    elif a == '4':
        first = input("input first symbol: ")
        second = input("input second symbol: ")
        if first.isalpha() or first == ' ' and second.isalpha() or second == ' ':
            decipher.change_symbols(first, second)
    elif a == '5':
        text = decipher.key_to_text()
        with open("code2_key.txt", 'w', encoding='utf-8') as file:
            file.write(text)
        with open("code2_deciphered.txt", 'w', encoding='utf-8') as file:
            file.write(decipher.de_text)
    elif a == '6':
        break
    print("\n")
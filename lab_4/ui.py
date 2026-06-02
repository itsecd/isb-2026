from tkinter import Tk, INSERT, END, Button, Label, Text
from tkinter import Menu
from hashing import deserialize, get_file_hash
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter.scrolledtext import ScrolledText


class App:
    def __init__(self, settings: dict, hash_db: dict, refresh_speed=33):
        self.window = Tk()
        self.refresh_speed = refresh_speed
        self.settings = settings
        self.hash_db = hash_db
        self.file_path = None
        self.file_data = None
        self.init_ui()
    
    def init_ui(self):
        self.window.title("Лабораторная работа №4")
        self.window.geometry("700x500")

        self.menu = Menu(self.window)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Загрузить', command=self.load_file)
        #self.file_menu.add_command(label='Загрузить', command=self.load_save_from_file)
        self.menu.add_cascade(label='Файл', menu=self.file_menu)
        self.window.config(menu=self.menu)

        self.file_label = Label(self.window, width=85, text="Нет открытого файла")
        self.file_label.grid(row=0, column=0, columnspan=2)

        self.textfield = ScrolledText(self.window, wrap="word", width=85)
        self.textfield.configure(state='disabled')
        self.textfield.grid(row=1, column=0, columnspan=2)

        self.hash_button = Button(self.window, text="Вычислить хэш", command=self.hash_button_handler)
        self.hash_button.grid(row=2, column=0)
        self.hash_button.configure(state='disabled')

        self.check_button = Button(self.window, text="Сравнить хэш", command=self.check_button_handler)
        self.check_button.grid(row=2, column=1)
        self.check_button.configure(state='disabled')

        self.hash_label = Text(self.window, width=85, height=1, borderwidth=0)
        self.hash_label.grid(row=3, column=0, columnspan=2)
        self.hash_label.configure(state='disabled')
        self.hash_label.configure(bg=self.window.cget('bg'), relief="flat")

        self.window.mainloop()


    def load_file(self):
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/")
        if filename:
            try:
                data = deserialize(filename)
                self.file_data = data
                self.file_path = filename
                self.file_label["text"] = f"Открыт: {self.file_path}"
                self.hash_button.configure(state='normal')
                self.check_button.configure(state='normal')

                self.textfield.configure(state='normal')
                self.textfield.delete("1.0", END)
                self.textfield.insert(INSERT, str(data, encoding="utf-8"))
                self.textfield.configure(state='disabled')
            except UnicodeDecodeError as e:
                self.textfield.configure(state='normal')
                self.textfield.delete("1.0", END)
                self.textfield.insert(INSERT, "<Не удалось открыть файл, как текст.>")
                self.textfield.configure(state='disabled')
            except Exception as e:
                    mb.showerror("Ошибка", "Произошла ошибка при загрузке файла!")
                    print(type(e), e)


    def hash_button_handler(self):
        if self.file_data:
            hash = get_file_hash(self.file_data, self.settings["hash_algorithm"])

            self.hash_label.configure(state='normal')
            self.hash_label.delete("1.0", END)
            self.hash_label.insert(1.0, f"Хеш: {hash}")
            self.hash_label.configure(state='disabled')
    
    def check_button_handler(self):
        if self.file_data:
            hash = get_file_hash(self.file_data, self.settings["hash_algorithm"])
            if self.file_path in self.hash_db.keys():
                if hash == self.hash_db[self.file_path]:
                    mb.showinfo("Успешно", "Хеши файлов совпадают!")
                else:
                    mb.showwarning("Предупреждение", "Хеши файлов НЕ совпадают!")
            else:
                self.hash_db[self.file_path] = hash
                mb.showinfo("Новый файл", "Хеш занесён в базу")
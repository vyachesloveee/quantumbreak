from tkinter import *
from tkinter import Tk
from tkinter import filedialog as fd 
from tkinter import messagebox as mb


class Window:
    #создание окна
    def __init__(self):
        self.root = Tk()
        self.root.title("  mercury")
        self.root.geometry('400x300')
        self.root.iconbitmap('mercury.ico')
        self.root.resizable(False, False)

    def run(self):
        self.callback()
        self.btn_click
        self.root.mainloop()

    def enter(self):
        mass = Tk.Entry(self.root, bd = 2)
        mass.place(x = 50, y = 10, width = 90)
        
    #создание меню
    '''
    def draw_menu(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label = 'Открыть файл', command = self.callback)
        file_menu.add_command(label = 'Экспортировать')
        file_menu.add_command(label = 'Выйти', command= self.exit)
        menu_bar.add_cascade(label = 'Файл', menu = file_menu)
        self.root.configure(menu = menu_bar)
    '''
    def exit(self):
        choice = mb.askyesno('Выход', 'Вы действительно хотите выйти?')
        if choice:
            self.root.destroy()

    def callback(self):
        name = fd.askopenfilename()
        print(name)
        return name
    
    def btn_click(self):
        mass1Input = Entry( self.root, bg = "white")
        mass1Input.pack()
        mass2Input = Entry( self.root, bg = "white")
        mass2Input.pack()
        voltInput = Entry( self.root, bg = "white")
        voltInput.pack()
        mass1 = mass1Input.get()
        mass2 = mass2Input.get()
        volt = voltInput.get()
        button = Button(self.root, text = 'Ввести')
        return mass1, mass2, volt

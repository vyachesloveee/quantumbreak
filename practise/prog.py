import xlsxwriter
from tkinter import *
from tkinter import filedialog as fd 
from tkinter import messagebox as mb
from tkinter import Tk, ttk
import re

row = 1
col = 0
i = 0
 
class Window:
    #создание окна
    def __init__(self):
        self.root = Tk()
        self.root.title("  mercury")
        self.root.geometry('400x300')
        self.root.iconbitmap('mercury.ico')
        self.root.resizable(False, False)

    def run(self):
        self.draw_menu()
        self.callback()
        self.root.mainloop()

    def enter():
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

window = Window()
temp_path = window.callback()
path = temp_path
print (path)
i = temp_path.rfind("/") # находит последний знак и возвращает его индекс
temp_path = temp_path[:i+1] # сохраняем путь включая этот индекс. т.е получаем нашу дирректорию
workbook = xlsxwriter.Workbook(temp_path +'cv.xlsx')
worksheet = workbook.add_worksheet()
start_line_number = 0

#Считывание файла, определение типа работы
class Calculations:
    def __init__(self, inline):
        self.line = inline
        self.values = 0
        pass

    def work_mode(self):
        flag = 0
        if "Тип работы" in self.line:
            flag = 1
        return self.line[12:], flag
    
    def sweep_rate(self):
        if 'Скорость развертки:' in self.line:
            if ',' in self.line:
                self.line = self.line.replace(',', '.')
            self.line = re.sub("\D", "", self.line)
            self.values = float(self.line)
        return self.values

    def current(self):
        while "Время," not in self.line:
            print(file.readline())
        values = self.line.split()
        specific_current = values[2]/ average_m
        values.append(specific_current)

    #подсчет средней массы
    def input_values(self, mass1 = 0.0128, mass2 = 0.0128, voltage = 0.8):
        average_m = (mass1 + mass2) / 2
        voltage = voltage
        return average_m, voltage


temp_array = [0, 0, 0, 0, 0]
sum_capacity = 0


with open(path, 'r') as file:
    flag = 0
    while flag == 0:
        line = file.readline()
        calc = Calculations(line)
        mode = calc.work_mode()[0]
        flag = calc.work_mode()[1]
    print(mode)

    while True:
        #Промотка до нужной строки
        while True:
            line = file.readline()
            if 'Скорость развертки:' in line:
                if ',' in line:
                    line = line.replace(',', '.')
                for i in line.split():
                    try:
                        #trying to convert i to float
                        sweep_rate = float(i)
                        #break the loop if i is the first string that's successfully converted
                        break
                    except:
                        continue
                print(sweep_rate)

            if "Время," in line:
                break

        #чтение и запись строк
        while True:
            line1 = file.readline()
            if line1 == '\n':
                break
            values = line1.split()
            for i in range (len(values)):
                if ',' in values[i]:
                    values[i] = values[i].replace(',', '.')
                values[i] = float(values[i])
#подсчет среднего тока
            if len(values)  < 3:
                break
            specific_current = values[2]/ calc.input_values()[0]
            values.append(specific_current)
#подсчет удельной емкости
            specific_capacity = values[3] * 2 / sweep_rate
            values.append(specific_capacity)
#подсчет заряда
            charge = (abs(temp_array[2]) + abs(values[2]))/2*(values[0]-temp_array[0])
            values.append(charge)
            print(values)
            sum_capacity = sum_capacity + charge
            temp_array = values
            for i in range(len(values)):
                worksheet.write(row, col + i, values[i])
            row +=1
        sum_capacity = sum_capacity/(2*calc.input_values()[1])
        worksheet.write(0, col + 6, 'Ёмкость')
        worksheet.write(2, col + 6, 'удельная ёмкость')
        worksheet.write(3, col + 6, 2*sum_capacity/calc.input_values()[0])
        worksheet.write(1, col + 6, sum_capacity)
        worksheet.write(4, col + 6, 'скорость развертки')
        worksheet.write(5, col + 6, sweep_rate)
        worksheet.write(0, col, 'Время, с' )
        worksheet.write(0, col+1, 'Потенциал, В ' )
        worksheet.write(0, col+2, 'Ток, А' )
        worksheet.write(0, col+3, 'Удельный ток, А/г' )
        worksheet.write(0, col+4, 'Удельная емкость, Ф/г' )
        worksheet.write(0, col+5, 'Заряд, Кл' )
        row = 1
        col = col + 8

        print(sum_capacity)
        raw = '1'
        '''
        print('Hit the enter button')
        while raw != '':
            raw = input()
            if raw != '':
                print('try again')
        '''
        sum_capacity = 0
        temp_array = [0, 0, 0, 0, 0]
        start_line_number = 6
        for i in range(start_line_number):
            print(file.readline())
        if line1 == '':
            print('end')
            break    
workbook.close()



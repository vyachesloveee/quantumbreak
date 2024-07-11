import xlsxwriter
from tkinter import *
from tkinter import filedialog as fd 
from tkinter import messagebox as mb
from tkinter import Tk, ttk

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
        
    #создание меню
    def draw_menu(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label = 'Открыть файл', command = self.callback)
        file_menu.add_command(label = 'Экспортировать')
        file_menu.add_command(label = 'Выйти', command= self.exit)
        menu_bar.add_cascade(label = 'Файл', menu = file_menu)
        self.root.configure(menu = menu_bar)
    
    def exit(self):
        choice = mb.askyesno('Выход', 'Вы действительно хотите выйти?')
        if choice:
            self.root.destroy()

    def callback(self):
        name= fd.askopenfilename()
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


class File:
    def __init__(self, name: str, counter):
        self.filename = name
        self.counter = counter
    
    def __enter__(self):
        with open(self.filename) as file:
            for i in range(self.counter + 1):
                self.line = file.readline()
        return self.line

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

for i in range(20):        
    with File(path, i) as file:
        line = file
        print(line)


#Считывание файла, определение типа работы
class Calculations:
    def __init__(self):
        pass
        
    def work_mode(self, path):
        with open(path, 'r') as file:
            while True:
                line = file.readline()
                if 'Тип работы:' in line:
                    work_mode = line[12:]
                    print(line[12:])
                    break
        return work_mode; 

    def sweep_rate(self):
        while True:
            line = file.readline() #print
            print(line)
            if 'Скорость развертки:' in line:
                sweep_rate = line[20:-6]
                if ',' in sweep_rate:
                    sweep_rate = sweep_rate.replace(',', '.')
                sweep_rate = float(sweep_rate)
            if 'Время,' in line:
                break
        return sweep_rate
        
    def calculus(self, average_m, voltage, sweep_rate, ):
        return 0

    def scroll(self):
        return 0

    #подсчет средней массы
    def input_values(self, mass1 = 0.0128, mass2 = 0.0128, voltage = 0.8):
        average_m = (mass1 + mass2) / 2
        voltage = voltage
        return average_m, voltage




'''
for i in range(2):
    print("Введите массу электрода", i+1)
    input_value = input()
    if ',' in input_value:
        input_value = input_value.replace(',', '.')
    average_m = average_m + float(input_value)/2
#Ввод рабочего напряжения
print('Введите рабочее напряжение в милливольтах')
input_value = input()
if ',' in input_value:
        input_value = input_value.replace(',', '.')
voltage = input_value/1000
'''




temp_array = [0, 0, 0, 0, 0]
sum_capacity = 0

calculations = Calculations()
mode = calculations.work_mode(temp_path)
print (mode)
calculations.sweep_rate()

#запись данных
with open(path, 'r') as file:
    while True:
        
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
            specific_current = values[2]/ average_m
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
        sum_capacity = sum_capacity/(2*voltage)
        worksheet.write(0, col + 6, 'Суммарный заряд')
        worksheet.write(1, col + 6, sum_capacity)
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

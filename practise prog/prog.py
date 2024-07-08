import xlsxwriter
import tkinter as tk
from tkinter import filedialog as fd 
from tkinter import Tk, ttk

row = 1
col = 0


i = 0
file_name = ''

def callback():
    name= fd.askopenfilename()
    return name

path = callback()
errmsg = 'Error!'

if '.txt' in path:
    l=-4
elif '.xlsx':
    l=-5

while True:
    if path[i] == '/':
        print(i)
        break
    i = i -1
file_name = path[i+1:-l] + '.xlsx'
workbook = xlsxwriter.Workbook('cv.xlsx')
worksheet = workbook.add_worksheet()
start_line_number = 0

#Считывание файла, определение типа работы
with open(path, 'r') as file:
    while True:
        line = file.readline()
        if 'Тип работы:' in line:
            work_mode = line[12:]
            start_line_number = i + 15
            print(line[12:])
        if 'Скорость развертки:' in line:
             sweep_rate = float(line[20])
             break
        i = i + 1

#подсчет средней массы
average_m = 0.0128
voltage = 0.8
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
line1='0'
j=0
voltage = 0.800
average_m = 0.0128
temp_array = [0, 0, 0, 0, 0]
sum_capacity = 0
#запись данных
with open(path, 'r') as file:
    while True:
        #Промотка до нужной строки
        for i in range(start_line_number):
            print(file.readline())
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
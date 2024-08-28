import xlsxwriter
from tkinter import *
from tkinter import filedialog as fd 
from tkinter import Tk
import re
import numpy as np
import pandas as pd
import datetime as dt
import easygui as e
row = 1
col = 0
i = 0
 

class Window:
    #создание окна
    def __init__(self):
        self.root = Tk()
        self.root.title("  mercury")
        self.root.geometry('400x300')
        self.root.resizable(False, False)
        self.mass1Input = Entry( self.root)
        self.mass2Input = Entry( self.root)
        self.voltInput = Entry( self.root)
        self.button = Button(self.root, text = "ввод", command= self.instance)
        self.button.grid(row=6, column=0, sticky=W)
        self.lable1=Label(self.root, text='введите массу 1 в граммах').grid(row=0, column=0, sticky=W)
        self.mass1Input.grid(row=1, column=0, sticky=W)
        self.lable2=Label(self.root, text='введите массу 2 в граммах').grid(row=2, column=0, sticky=W)
        self.mass2Input.grid(row=3, column=0, sticky=W)
        self.lable3=Label(self.root, text='введите рабочее напряжение в милливольтах').grid(row=4, column=0, sticky=W)
        self.voltInput.grid(row=5, column=0, sticky=W)
        self.root.mainloop()

    def callback(self):
        name = fd.askopenfilename()
        print(name)
        return name
    
    def instance(self):
        mass1 = self.mass1Input.get()
        mass2 = self.mass2Input.get()
        volt = self.voltInput.get()
        global insertion
        insertion = [float(mass1), float(mass2), float(volt)]
        self.root.quit()

    




random = str(dt.datetime.now())+'.xlsx'
if ':' in random:
    random = random.replace(':', '-')
window = Window()
temp_path = window.callback()

print(insertion)
path = temp_path
print (path)



i = temp_path.rfind("/") # находит последний знак и возвращает его индекс
temp_path = temp_path[:i+1] # сохраняем путь включая этот индекс. т.е получаем нашу дирректорию
workbook = xlsxwriter.Workbook(temp_path +random)
worksheet = workbook.add_worksheet()
start_line_number = 0

#Считывание файла, определение типа работы
class Calculations:
    def __init__(self, inline, mass1, mass2, voltage):
        self.line = inline
        self.values = 0
        self.avmass = (mass1 + mass2) / 2 
        self.voltage = voltage
        pass

    def work_mode(self): 
        flag = 0 
        if "Потенциостат" in self.line:
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
        specific_current = values[2]/ self.mass
        values.append(specific_current)

    def input_values(self):
        average_m = self.avmass
        voltage = self.voltage
        return average_m, voltage
charge = 0
sum_capacity = 0
sum_capacity1 = 0
sum_capacity2 = 0
time = 0
df = pd.DataFrame(columns=['time', 'potential', 'current', 'specific_current', 'specific_capacity', 'charge'])
j=0
f=0
with open(path, 'r') as file:
    flag = 0 
    while f < 1:
        line = file.readline()
        calc = Calculations(line, insertion[0], insertion[1], insertion[2])
        mode = calc.work_mode()[0]
        flag = calc.work_mode()[1]
        f = f + 1

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
            if line1 == '\n' or line1 == '':
                break 
            values = line1.split()

            for i in range (len(values)):
                if ',' in values[i]:
                    values[i] = values[i].replace(',', '.')
                values[i] = float(values[i])
            values.extend([0,0,0])
            df.loc[len(df.index)] = values  
            worksheet.write(j, col, df.loc[j, 'time'] )
            worksheet.write(j, col+1, df.loc[j, 'potential'] )
            worksheet.write(j, col+2, df.loc[j, 'current'] )
            if len(df) > 3:
                if abs(df.loc[j-3, 'current'] - df.loc[j-2, 'current'] / df.loc[j-3, 'current']) > 0.30:
                    df.loc[j-2, 'current'] = (df.loc[j-3, 'current'] + df.loc[j, 'current'])/2

#подсчет среднего тока
            if values[3] !=0:
                break
            df.loc[j, 'specific_current'] = df.loc[j, 'current']/ calc.input_values()[0]
            worksheet.write(j, col+3, df.loc[j, 'specific_current'] )
#подсчет удельной емкости
            df.loc[j, 'specific_capacity'] = df.loc[j, 'specific_current'] * 2 / sweep_rate
            worksheet.write(j, col+4, df.loc[j, 'specific_capacity'] )
#подсчет заряда
            if len(df) > 1:
                df.loc[j, 'charge'] = (abs(df.loc[j, 'current']) + abs(df.loc[j-1, 'current']))*(df.loc[j, 'time']-df.loc[j-1, 'time'])/2
                #sum_capacity1 = sum_capacity1 + (df.loc[j, 'current'] + df.loc[j-1, 'current'])*(df.loc[j, 'potential'] - df.loc[j-1, 'potential'])
                worksheet.write(j, col+5, df.loc[j, 'charge'] )

                if df.loc[j-1, 'current']>=0 and df.loc[j, 'current'] <= df['current'].max():
                    sum_capacity2 = sum_capacity2 + df.loc[j, 'charge']/(2 * calc.input_values()[1])
                    time = df.loc[j, 'time'] 
                if df.loc[j, 'time'] > time and df.loc[j-1, 'current'] < 0 :
                    sum_capacity2 = sum_capacity2 + df.loc[j, 'charge']/(2 * calc.input_values()[1])  
            row +=1
            j=j+1
        if line1 == '':
            break 
#создание xls

        worksheet.write(0, col + 6, 'Ёмкость, Ф')
        worksheet.write(2, col + 6, 'Удельная ёмкость, Ф/г')
        worksheet.write(3, col + 6, 1000*2*sum_capacity2/calc.input_values()[0])
        worksheet.write(1, col + 6, 1000*sum_capacity2)
        worksheet.write(4, col + 6, 'Скорость развертки, В')
        worksheet.write(5, col + 6, sweep_rate)
        worksheet.write(0, col, 'Время, с' )
        worksheet.write(0, col+1, 'Потенциал, В ' )
        worksheet.write(0, col+2, 'Ток, А' )
        worksheet.write(0, col+3, 'Удельный ток, А/г' )
        worksheet.write(0, col+4, 'Удельная емкость, Ф/г' )
        worksheet.write(0, col+5, 'Заряд, Кл' )
        row = 1
        col = col + 8
        start_line_number = 6
        for i in range(start_line_number):
            print(file.readline())
        if line1 == '':
            print('end')
            break    
workbook.close()


 
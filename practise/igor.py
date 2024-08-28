def read_previous_line(file):
    current_pos = file.tell()  # Сохраняем текущую позицию указателя
    if current_pos == 0:
        return None  # В начале файла, предыдущей строки нет

    # Перемещаемся назад по одной позиции, чтобы найти начало текущей строки
    file.seek(current_pos - 1)

    # Ищем начало предыдущей строки
    while current_pos > 0:
        file.seek(current_pos - 1)  
        char = file.read(1)
        if char == "\n":
            break
        current_pos -= 1 

    if current_pos > 0:
        file.seek(current_pos)  # Перемещаемся в начало предыдущей строки
    else:
        file.seek(0)  # Если достигли начала файла, перемещаемся туда

    return file.readline()  # Читаем предыдущую строку 


with open('yourfile.txt', 'r') as file:
    # Читаем строки по одной
    line1 = file.readline()
    line2 = file.readline()
    print("Current line:", line2.strip())

    # Возвращаемся на одну строку назад
    prev_line = read_previous_line(file) 
    print("Previous line:", prev_line.strip())

    # Прочитать текущую строку снова
    current_line_again = file.readline()
    print("Current line again:", current_line_again.strip())
 
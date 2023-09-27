#Комментирование
#Ctrl-K + Ctrl-C
#Расскомментирование
#Ctrl-K + Ctrl-U

import datetime     #Время выполнения
import array        #Работа с массивами
import random       #Для генерации случайного цвета для диаграммы
import pandas as pd #Сбор структуры для построения диаграммы
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num, DateFormatter, DayLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import Patch
import numpy as np
import time         #Время выполнения кода
import os.path      #Работа с файлами

#Чтение данных из файла
def read_file():
    if (os.path.exists("dannie.txt")):  #Проверка существования файла
        file1 = open("dannie.txt", "r")
        i=0;    #Общее количество деталей
        while True: #пока строка не пуста, выполнять разбор
            line = file1.readline() #Считывание строки из файла
            if not line:    #Строка пустая
                break       #Выход из цикла
            #Заполнение данными из файла матрицы
            arr = line.split()  #распределение строки из файла в массив

            dannie.append([0]*(len(arr) + 1))    #динамическое расширение массива данных
            dannie1.append([0]*(len(arr) + 1))   #динамическое расширение массива данных

            dannie[i][0] = i    #заполнение номера строки
            for u in range(len(arr)):
                dannie[i][u + 1] = int(arr[u])
            dannie1[i] = dannie[i]      #Копирование исходных данных для дальнейшего восстановления последовательности деталей (по индексам)
            i = i + 1  
    
        num_det = i #Общее количество деталей
        return True #Успешное чтение данных из файла
    else:
        print("Ошибка открытия файла")
        return False #Чтение файла завершилось с ошибкой

#Вывод матрицы
def print_matrx(dannie_vivod):
    for i in range(len(dannie_vivod)):
        for j in range(len(dannie_vivod[i])):
            print(dannie_vivod[i][j], end=" ")
            if (j == 0):
                print("| ", end="")
        print() #Снос строки

#Расчет простоя станка
def prostoi_stanka(dannie_info):
    TMinOld = int(dannie_info[0][1])
    for y in range(len(dannie_info) - 1):
        TMinOld = int(TMinOld) + int(dannie_info[y + 1][1]) - int(dannie_info[y][2])
    return TMinOld  #Возврат времени простоя

#Генерация случайного цвета для графика
def get_color():
    return('#' + ''.join([random.choice('ABCDE1234567890') for i in range(6)]))

#Сортировка методом Джонсона
def sort_Johnson(dannie_sort):
    verh = 0    #Первая строка
    niz = len(dannie_sort)   #Последняя строка

    while (len(dannie_sort) > 0):
        #У  становка начальных значений для переменных
        func = 0
        num =  0
        min = dannie_sort[0][1]
        j=0
        i=0
        for j in range(2):
            for i in range(len(dannie_sort)):
                if ((min == dannie_sort[i][j + 1] and func == 2) or (min > dannie_sort  [i][j + 1])):
                    min = dannie_sort[i][j + 1]    
                    func = j + 1    #если найдено по A, то func == 0, иначе func == 1
                    num = i #строка с минимальным значением
        
        #перенос строки из исходной матрицы в новую
        if (func == 1):
            dannie1[verh] = dannie_sort[num]
            verh = verh + 1
        else:
            niz = niz - 1
            dannie1[niz] = dannie_sort[num]
        
        #удаление строки, в которой найден минимальный элемент
        dannie_sort.remove(dannie_sort[num])

def create_struct(dannie_str, color_mass):
    #массивы для создания структуры
    task = []       #Наименование станка
    color = []      #Цвет на диаграмме
    start = []      #Время начала обработки n детали
    end = []        #Время окончания обработки n детали
    task_d = []     #Длительность обработки n детали

    for i in range (2 * len(dannie_str)):
        task.append([])
        color.append([])
        start.append([0])
        end.append([0])
        task_d.append([0])


    for i in range(len(dannie_str)):
        task[i] = "A"
        task[i + len(dannie_str)] = "B"
    
        #color[i] = color[i + len(dannie_str)] = get_color()   #заполение цветами
        color[i] = color[i + len(dannie_str)] = color_mass[dannie_str[i][0]]
        if (i == 0):
            start[i] = 0
            start[i + len(dannie_str)] = dannie_str[i][1]
            end[i] = start[i] + dannie_str[i][1]
            end[i + len(dannie_str)] = start[i + len(dannie_str)] + dannie_str[i][2]
        else:
            start[i]= end[i - 1]
            end[i] = start[i] + dannie_str[i][1]

            if (end[i] < end[i + len(dannie_str) - 1]):
                start[i + len(dannie_str)] = end[i + len(dannie_str) - 1]
            else:
                start[i + len(dannie_str)] = end[i]

            end[i + len(dannie_str)] = start[i + len(dannie_str)] + dannie_str[i][2]
    
            #Заполнение структуры
        task_d[i] = end[i] - start[i]
        task_d[i + len(dannie_str)] = end[i + len(dannie_str)] - start[i + len(dannie_str)]

    struct = pd.DataFrame({
        'task': task,
        'color': color,
        'start': start,
        'end': end,
        'task_duration': task_d
        })
    
    return struct

def gia_Gantt(data):
    fig, axs = plt.subplots(nrows = len(data), ncols = 1)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.35)

    fig.canvas.manager.set_window_title('Модель задачи Джонсона‐Белмана')

    for i in range(len(data)):
        axs[i].barh(y = data[i][0]['task'], width=data[i][0]['task_duration'], left=data[i][0]['start'], color=data[i][0]['color'])
        axs[i].invert_yaxis()
        axs[i].set_xlim([0, max(data[0][0]['end'][len(data[0][0]['end'])-1], data[0][0]['end'][len(data[0][0]['end'])-1])+3])

    axs[0].set_title("График Ганта с изначальными данными")
    axs[1].set_title("График Ганта с оптимальными данными")
    plt.show()

def generate_color(color_mass):
    color_mass.append('#' + ''.join([random.choice('ABCDE1234567890') for i in range(6)]))

color_massiv = []
dannie = []     #Исходные данные
dannie1 = []    #SORT JOHNSON (A, B)

if (read_file()):
    print("Исходный порядок обработки деталей: ")
    print_matrx(dannie)
    
    print("\nВремя простоя (при исходном порядке):", prostoi_stanka(dannie))

    #Структура данных для исходных данных
    dannie_temp = []
    dannie_temp = dannie

    #Заполнение цветового массива
    for i in range(len(dannie1)):
        generate_color(color_massiv)

    struct_start = create_struct(dannie,color_massiv)
    print(struct_start)
    #Создание структуры для оптимального варианта
    StartOldN2 = time.time() ## точка отсчета времени
    tic = time.perf_counter()
    
    sort_Johnson(dannie)    #Поиск оптимального порядка по методу Джонсона

    end = (time.time() - StartOldN2) * 1000 #Точка окончания отсчета времени
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.10f} секунд")

    print("\nОптимальная расстановка деталей (по методу Джонсона):")
    print_matrx(dannie1)
    
    print("\nВремя простоя (при оптимальном порядке, метод Джонсона):", prostoi_stanka(dannie1))

    

    struct_optimal1 = create_struct(dannie1, color_massiv)

    print("Общее время обработки деталей:")
    print(struct_optimal1['end']. values [len(dannie1) * (len(dannie1[0]) - 1) - 1])

    gia_Gantt([[struct_start],[struct_optimal1]])

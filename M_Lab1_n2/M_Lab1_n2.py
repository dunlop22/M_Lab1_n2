import datetime
import itertools    #итерации

import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num, DateFormatter, DayLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import Patch
import numpy as np
import time         ##Время выполнения кода
import os.path


def read_file():
    if (os.path.exists("dannie.txt")):
        file1 = open("dannie.txt", "r")
        i=0;
        while True:
            line = file1.readline() #Считывание строки из файла
            if not line:    #Строка пустая
                break       #Выход из цикла
            ##заполнение данными из файла матрицы
            arr = line.split()  #распределение строки из файла в массив

            dannie.append([0]*len(arr))    #динамическое расширение массива данных
            dannie1.append([0]*len(arr))   #динамическое расширение массива данных
            dannie_copy.append([0]*len(arr))

            dannie[i][0] = i    #заполнение номера строки
            for u in range(len(arr) - 1):
                dannie[i][u + 1] = int(arr[u])
            dannie1[i] = dannie[i]      #Копирование исходных данных для дальнейшего восстановления последовательности деталей (по индексам)
            dannie_copy[i] = dannie[i]
            i = i + 1  
    
        num_det = i #Общее количество деталей
        return True
    else:
        print("Ошибка открытия файла")
        return False

dannie = []     #Исходные данные
dannie_copy = []     #Исходные данные (для метода перебора)
dannie1 = []    #SORT JOHNSON (A, B, C)

if (read_file()):
    print("OK")



import datetime
import itertools    #итерации

import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num, DateFormatter, DayLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import Patch
import numpy as np
import time         ##Время выполнения кода
import os.path

#Чтение данных из файла
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

            dannie.append([0]*(len(arr) + 1))    #динамическое расширение массива данных
            dannie1.append([0]*(len(arr) + 1))   #динамическое расширение массива данных
            dannie_copy.append([0]*(len(arr) + 1))

            dannie[i][0] = i    #заполнение номера строки
            for u in range(len(arr)):
                dannie[i][u + 1] = int(arr[u])
            dannie1[i] = dannie[i]      #Копирование исходных данных для дальнейшего восстановления последовательности деталей (по индексам)
            dannie_copy[i] = dannie[i]
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

#Сортировка методом Джонсона
def sort_Johnson():
    ()

dannie = []     #Исходные данные
dannie_copy = []     #Исходные данные (для метода перебора)
dannie1 = []    #SORT JOHNSON (A, B)

if (read_file()):
    print_matrx(dannie)
    print("OK")  



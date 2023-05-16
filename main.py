import math
import csv
import numpy as np


"""
Функция для чтения csv файла из таблицы.
Преобразует файл в матрицу представленную двумерным
"""
def ReadCSV(file):
    CSVarr = []
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            CSVarr.append(row)
            print(', '.join(row))
        return CSVarr


def PrintTable():
    pass


def sort():
    pass


def search():
    pass


def Validator():
    pass


def totalRevenue(data):
    pass


def ProductShare(data):
    pass


def CreateReport(data):
    print("Общая выручка магазина составила:\n", totalRevenue(data))
    print("товар, который был продан наибольшее кол-во раз:\n")
    print("Товар, который принес наибольшую выручку:\n")
    PrintTable(data)
    ProductShare(data)


if __name__ == '__main__':
    data = ReadCSV('table.csv')
    CreateReport(data)
    print(np.array(data))
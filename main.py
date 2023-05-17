import math
import csv
import numpy as np
import heapq
from datetime import datetime, date


class Order:
    def __init__(self):
        self.Order = []


"""
Функция для чтения csv файла из таблицы.
Преобразует файл в двумерный массив, где каждый одномерный массив
является строкой из файла
"""
def read_csv(file):
    try:
        with open(file, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';', quotechar='|')
            csv_arr = []
            isFirst = True
            for row in reader:
                if isFirst:
                    isFirst = False
                    csv_arr.append(row)
                    continue
                validate(row)
                csv_arr.append(row)
            return csv_arr
    except IOError:
        print("Файл не открывается")


def partition(array, left, right):
    pivot = array[right]
    i = left
    j = right - 1
    while i < j:
        while (array[i] < pivot and i < right):
            i += 1
        while (array[j] >= pivot and j > left):
            j -= 1
        if i < j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    if array[i] > pivot:
        array[i], array[right] = array[right], array[i]
    return i


def quick_sort(array, start, end):
    if start < end:
        right_start = partition(array, start, end)
        quick_sort(array, start, right_start - 1)
        quick_sort(array, right_start + 1 , end)

"""
Функция запускающая сортировку для массива, сформированного по заданному
параметру, вовзращает отсортированный массив содержащий данные заданного параметра
"""
def sort_param(data, param):
    sort_arr = []
    for i in range(1, len(data)):
        sort_arr.append(int(data[i][param]))
    quick_sort(sort_arr, 0, len(sort_arr)-1)
    return sort_arr


def binary_search(arr, element):
    # обозначим элементы между которыми находится искомый
    first = 0
    last = len(arr)-1
    # Сдвигаем границы для поиска
    while first <= last:
        # Делим пополам
        mid = int((first + last)/2)
        # Условие выхода
        if arr[mid] == element:
            return mid
        # Если меньше среднего, сдвигаем правую границу
        elif element < arr[mid] :
            last = mid-1
        # Иначе левую
        else:
            first = mid+1
    return None



def search_param(data, element, param, param_index):
    result = []
    for i in range(1, len(data)):
        if data[i][param_index] == param:
            result.append(data[i][element])
    return result


"""
Функция проверки данных на валидность: 
- Итоговая сумма за все проданные единицы товара должна быть ровна произведению
- Дата заказа не может бфть позже текущей 
- Недопустимо отрицательное или нулевое кол-во товаров
- Недопустима нулевая или отрицательная цена за единицу товара или за весь
- преобразует строковые числа из файла в int тем самым проверяя их на тип
"""
def validate(arr):
    arr[0], arr[4], arr[5], arr[6] = int(arr[0]), int(arr[4]), int(arr[5]), int(arr[6])
    if arr[4] <= 0:
        raise Exception("Отрицательное или нулевое кол-во товара")
    if arr[5] <= 0:
        raise Exception("Отрицательная или нулевая цена за товар")
    if arr[6] <= 0:
        raise Exception("Отрицательная или нулевая итоговая цена")
    if arr[4]*arr[5] != arr[6]:
        raise Exception("Итоговая цена неверно посчитана")
    date_object = datetime.strptime(arr[1], "%d.%m.%Y").date()
    if date_object > date.today():
        raise Exception("Дата добавления превышает текущую")


def total_revenue(data):
    total_sum = 0
    for i in range(1, len(data)):
        total_sum += int(data[i][6])
    return total_sum


def best_product(data, param):
    arr = sort_param(data, param)
    max_amount = arr[-1]
    return search_param(data, 2, max_amount, param)


def best_total(arr, param):
    #data = {}
    #data['key'] = value
    pass

def print_table(arr):
    pass


def product_share(data):
    pass


def create_report(data):
    print("Общая выручка магазина составила:\n", total_revenue(data))
    print("товар(ы), который/ые был(и) продан(ы) наибольшее кол-во раз:\n", best_product(data, 4))
    print("Товар(ы), который/ые принес(ли) наибольшую выручку:\n", best_product(data, 6))
    print_table(data)
    product_share(data)


if __name__ == '__main__':
    data = read_csv('table.csv')
    create_report(data)
    #print(np.array(data))
    for i in range(len(data)):
        print(data[i])



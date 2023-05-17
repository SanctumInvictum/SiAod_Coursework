import csv
from datetime import datetime, date
from tabulate import tabulate


class Node:
    """
    Реализация структуры данных узла для структуры хэш-таблицы
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    Структура данных - хэш таблица с рехешированием через метод цепочек
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def insert(self, key, value):
        index = hash(key) % self.capacity
        node = self.buckets[index]
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node

    def get(self, key):
        index = hash(key) % self.capacity
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None


def read_csv(file):
    """
    Функция для чтения csv файла из таблицы.
    Преобразует файл в двумерный массив, где каждый одномерный массив
    является строкой из файла
    """
    try:
        with open(file, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';', quotechar='|')
            csv_arr = []
            is_first = True
            for row in reader:
                if is_first:
                    is_first = False
                    continue
                validate(row)
                csv_arr.append(row)
            return csv_arr
    except IOError:
        print("Файл не открывается")


def validate(arr):
    """
    Функция проверки данных на валидность:
    - Итоговая сумма за все проданные единицы товара должна быть ровна произведению
    - Дата заказа не может бфть позже текущей
    - Недопустимо отрицательное или нулевое кол-во товаров
    - Недопустима нулевая или отрицательная цена за единицу товара или за весь
    - преобразует строковые числа из файла в int тем самым проверяя их на тип
    """
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


def partition(array, left, right, param):
    """
    Часть алгоритма быстрой сортировки Хоара
    Выделяет опорный элемент - pivot и по нему пересобирает массив в следующем виде:
    элементы меньше опорного, опорный, элементы больше опорного
    """
    pivot = array[right][param]
    i = left
    j = right - 1
    while i < j:
        while array[i][param] < pivot and i < right:
            i += 1
        while array[j][param] >= pivot and j > left:
            j -= 1
        if i < j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    if array[i][param] > pivot:
        array[i], array[right] = array[right], array[i]
    return i


def quick_sort(array, start, end, param):
    """
    Основная функция быстрой сортировки Хоара. Вызывает partition разделяя массив по опорному элементу,
    затем рекурсивно вызывает себя дважды для элементов слева от опорного и справа от опорного, пока не распределит
    все элементы в правильном порядке
    """
    if start < end:
        right_start = partition(array, start, end, param)
        quick_sort(array, start, right_start - 1, param)
        quick_sort(array, right_start + 1, end, param)


def sort_param(data, param):
    """
    Функция вызывающая сортировку для массива по заданному параметру и возвращающая отсортированную копию данных
    параметр:
    - 0 номер заказа
    - 4 кол-во продаж
    - 5 цена за единицу
    - 6 общая стоимость
    """
    sort_arr = data
    quick_sort(sort_arr, 0, len(sort_arr)-1, param)
    return sort_arr


def revenue(data, param):
    """
    Функция, суммирующая элементы по параметру
    """
    total_sum = 0
    for i in range(len(data)):
        total_sum += int(data[i][param])
    return total_sum


def best_product(data, param):
    """
    Функция, вызывающая сортировку по параметру и возвращающая имя по наибольшему значению параметра
    """
    return sort_param(data, param)[-1][2]


def print_table(data, total_table, amount_table):
    """
    Функция печати аккуратной таблицы, принимает наименования товаров из данных, хэш-таблицу долей
    и хэш-таблицу количетсва проданного товара и через хэш-поиск по ключу-наименованию товара добавляет в итоговую
    таблицу соответствующие значения кол-ва проданного товара и его доли от общей прибыли
    """
    table = [['Название товара', 'Количество продаж', 'Доля товара, %']]
    for row in data:
        table.append([row[2], amount_table.get(row[2]), round(total_table.get(row[2]),3)])

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def product_share(data, venue):
    """
    Функция, формирующая хэш-таблицу со связью наименований товаров с их долей в процентах от общей суммы продаж
    """
    arr = list(reversed(data))
    table = HashTable(len(arr))
    for i in range(len(arr)):
        table.insert(arr[i][2], arr[i][6]/(venue/100))
    return table


def create_report(data):
    """
    Функция, формирующая отчет по всем требуемым заданиям
    """
    total_revenue = revenue(data, 6)
    best_amount = best_product(data, 4)
    best_total = best_product(data, 6)
    print("Общая выручка магазина составила:\n", total_revenue,"у.е.\n-------------------------------------")
    print("товар, проданный наибольшее кол-во раз:\n", best_amount, "\n-------------------------------------")
    print("Товар, принесший наибольшую выручку:\n", best_total, "\n-------------------------------------")
    amount_table = HashTable(len(data))
    for i in range(len(data)):
        amount_table.insert(data[i][2], data[i][4])
    print_table(data, product_share(sort_param(data, 6), total_revenue), amount_table)


if __name__ == '__main__':
    data = read_csv('table.csv')
    create_report(data)
    for i in range(len(data)):
        print(data[i])



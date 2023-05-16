import math
import csv
import numpy as np

def ReadCSV(file):
    CSVarr = []
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            CSVarr.append(row)
            print(', '.join(row))
        return CSVarr
def sort():
    pass

def search():
    pass

def CreateReport(data):
    pass

if __name__ == '__main__':
    data = ReadCSV('table.csv')
    CreateReport(data)
    print(np.array(data))
import tushare as ts
import pandas as pd
import time
import datetime
import csv
import os.path
import matplotlib.pyplot as plt

g_profitFileName = 'C:/python/csv/zhangting/profit.csv'
g_dirProfit = {}
#('000020.SZ', '2020-01-01', 9.5)
def saveParaToCsv(ts_code, date, profit):
    isFileExist = os.path.isfile(g_profitFileName)
    with open(g_profitFileName, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])

def calculateProfit(fileName):
    global g_dirProfit
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['date'] not in g_dirProfit:
                g_dirProfit[row['date']] = float(row['profit'])
            else:
                g_dirProfit[row['date']] = g_dirProfit[row['date']] + float(row['profit'])
    g_dirProfit = sorted(g_dirProfit.items(), key=lambda d: d[0], reverse=False)
    print(g_dirProfit)

def saveFile():
    saveParaToCsv('000020.SZ', '2020-01-01', 3)
    saveParaToCsv('000030.SZ', '2020-01-01', 5)
    saveParaToCsv('000020.SZ', '2020-01-03', 8)
    saveParaToCsv('000030.SZ', '2020-01-03', 10)
    saveParaToCsv('000040.SZ', '2020-01-02', 33)
    saveParaToCsv('000020.SZ', '2020-01-01', 20)

calculateProfit(g_profitFileName)

def drawPic():
    print(g_dirProfit)
    x1 = list(g_dirProfit.keys())
    y1 = list(g_dirProfit.values())
    plt.plot(x1, y1, label='Frist line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('Plot Number')
    plt.ylabel('Important var')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.show()

dic = {}
a = 'lyw'
dic[a] = 2
print(dic)
print(list(dic.keys()))
#drawPic()

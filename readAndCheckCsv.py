import tushare as ts
import pandas as pd
import time
import datetime
import csv
import os.path
#画图显示
import matplotlib.pyplot as plt
from pylab import mpl #正常显示画图时出现的中文
mpl.rcParams['font.sans-serif']=['SimHei'] #这里使用微软雅黑字体
mpl.rcParams['axes.unicode_minus']=False #画图时显示负号

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
    g_dirProfit = {}
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            value = row['profit']
            if date not in g_dirProfit:
                g_dirProfit[date] = float(value)
            else:
                g_dirProfit[date] = g_dirProfit[date] + float(value)
    #print(g_dirProfit)
    g_dirProfit = dict(sorted(g_dirProfit.items(), key=lambda d: d[0], reverse=False))
    #print(g_dirProfit)

def saveFile():
    saveParaToCsv('000020.SZ', '2020-01-01', 3)
    saveParaToCsv('000030.SZ', '2020-01-01', 5)
    saveParaToCsv('000020.SZ', '2020-01-03', 8)
    saveParaToCsv('000030.SZ', '2020-01-03', 10)
    saveParaToCsv('000040.SZ', '2020-01-02', 33)
    saveParaToCsv('000020.SZ', '2020-01-01', 20)

def drawProfitPic():
    print(g_dirProfit)
    totalProfit = 0
    averageProfit = 0
    x1 = list(g_dirProfit.keys())
    y1 = list(g_dirProfit.values())
    plt.plot(x1, y1, label='Frist line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('日期')
    plt.ylabel('收益率')
    for i in range(len(y1)):
        totalProfit += y1[i]
    averageProfit = round(totalProfit / len(y1), 2)
    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit))
    plt.legend()
    plt.show()

calculateProfit(g_profitFileName)
drawProfitPic()

import tushare as ts
import pandas as pd
import time
import datetime
import csv
import os.path
from datetime import datetime
#画图显示
import matplotlib.pyplot as plt
from pylab import mpl #正常显示画图时出现的中文
mpl.rcParams['font.sans-serif']=['SimHei'] #这里使用微软雅黑字体
mpl.rcParams['axes.unicode_minus']=False #画图时显示负号

g_profitFileName = 'C:/python/csv/zhangting/profit.csv'
g_dirProfit = {}
g_dirStock = {}
g_totalProfit = 0
#('000020.SZ', '2020-01-01', 9.5)
def saveProfitToCsv(ts_code, date, profit):
    writeMethod = 'w'
    isFileExist = os.path.isfile(g_profitFileName)
    if False == isFileExist:
        writeMethod = 'w'
    else:
        writeMethod = 'a'

    with open(g_profitFileName, writeMethod, encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])

def deleteProfitToCsv(name):
    if True == os.path.isfile(name):
        os.remove(name)

def calculateProfit(fileName):
    global g_dirProfit
    global g_totalProfit
    global g_dirStock
    g_dirProfit = {}
    dirtCount = {}
    if False == os.path.isfile(fileName):
        return;
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            value = row['profit']
            stock = row['ts_code']
            if date not in g_dirProfit:
                g_dirProfit[date] = float(value)
                dirtCount[date] = 1
                g_dirStock[date] = stock
            else:
                g_dirProfit[date] = g_dirProfit[date] + float(value)
                dirtCount[date] = dirtCount[date] + 1
                g_dirStock[date] = g_dirStock[date] + ',' + stock
    #print(g_dirProfit)
    g_dirProfit = dict(sorted(g_dirProfit.items(), key=lambda d: d[0], reverse=False))
    g_dirStock = dict(sorted(g_dirStock.items(), key=lambda d: d[0], reverse=False))
    g_totalProfit = 1
    for k in g_dirProfit:
        g_dirProfit[k] = round((g_dirProfit[k]) / dirtCount[k], 4)
        g_totalProfit = round(g_totalProfit*(1 + (g_dirProfit[k]/100)),2)
    print('g_dirStock = ' + str(g_dirStock))

def saveFileTest():
    saveProfitToCsv('000020.SZ', '2020-01-01', 3)
    saveProfitToCsv('000030.SZ', '2020-01-01', 5)

def drawProfitPic():
    localtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f'Draw profit picture at {localtime}')
    print(f'drawProfitPic,  g_dirProfit = {g_dirProfit}')
    totalProfit = 0
    averageProfit = 0
    if 0 == len(g_dirProfit):
        return;

    x1 = list(g_dirProfit.keys())
    y1 = list(g_dirProfit.values())
    plt.plot(x1, y1, label='Frist line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('日期')
    plt.ylabel('收益率')
    for i in range(len(y1)):
        totalProfit += y1[i]
    averageProfit = round(totalProfit / len(y1), 2)
    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit) + ', 总收益: ' + str(g_totalProfit))
    plt.legend()
    plt.show()

#calculateProfit(g_profitFileName)
#drawProfitPic()
#deleteProfitToCsv(g_profitFileName)

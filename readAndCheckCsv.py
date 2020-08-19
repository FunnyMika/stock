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

def saveLimitToCsv(fileName, date, ts_code):
    writeMethod = 'w'
    isFileExist = os.path.isfile(fileName)
    if False == isFileExist:
        writeMethod = 'w'
    else:
        writeMethod = 'a'

    with open(fileName, writeMethod, encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['date', 'ts_code'])
        writer.writerow([date, ts_code])

def deleteFile(name):
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
        g_totalProfit = round(g_totalProfit*(1 + (g_dirProfit[k]/100)),4)
    g_totalProfit = round((g_totalProfit - 1)*100, 4)
    #print('g_dirStock = ' + str(g_dirStock))

def getOpenLimitStockFromCsv(fileName):
    dirStock = {}
    if False == os.path.isfile(fileName):
        return;
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            stock = row['ts_code']
            if date not in dirStock:
                dirStock[date] = stock
            else:
                dirStock[date] = dirStock[date] + ',' + stock
    dirStock = dict(sorted(dirStock.items(), key=lambda d: d[0], reverse=False))

    print('dirStock = ' + str(dirStock))
    return dirStock

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
    startDate = '开始日期' + x1[0] + ', 结束日期' + x1[len(x1) - 1]
    temp1 = []
    for i in range(len(x1)):
        temp1.append(x1[i][6:8])
    x1 = temp1.copy()
    y1 = list(g_dirProfit.values())
    plt.plot(x1, y1, linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=2)
    for x, y in zip(x1, y1): #显示数值
        plt.text(x, y, '%.0f' % y, fontdict={'fontsize': 14})
    plt.xlabel(startDate)
    plt.ylabel('收益率')
    for i in range(len(y1)):
        totalProfit += y1[i]
    averageProfit = round(float(totalProfit) / len(y1), 2)
    #print(f'totalProfit={totalProfit}, len(y1)={len(y1)}, averageProfit={averageProfit},g_totalProfit={g_totalProfit}')
    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit) + '%, 总收益: ' + str(g_totalProfit)+'%')
    plt.legend()
    plt.show()

#calculateProfit(g_profitFileName)
#drawProfitPic()
#deleteFile(g_profitFileName)
import tushare as ts
import pandas as pd
import csv
import time
import datetime
import os.path
import os
import downloadFile
import sys

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')

#下载上一个交易日所有股票的收盘价和前一天的收盘价
def downloadDailyToCsv(Date, fielName):
    if True == os.path.isfile(fileName):
        os.remove(fileName)

    pro = ts.pro_api()
    try:
        df = pro.daily(trade_date=Date, fields='ts_code, close, pre_close')
        listAllStocks = []
        df.to_csv(fileName, mode='a', header=True)
    except:
        print(f'get yesterday stock fail!')

#获得上一个交易日日期
def getLastTradeDate():
    date = time.strftime("%Y%m%d", time.localtime())
    #print(date)
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=date, end_date=date, fields = 'cal_date, pretrade_date')
    #print(df)
    print(df.iloc[0,1])
    return df.iloc[0,1]

def getYesterdayData():
    fileName = os.getcwd() + '\yesterdayData.csv'
    fileName = fileName.replace('\\', '/')
    listLimitStock = []

    Date = getLastTradeDate()

    if False == os.path.isfile(fileName):
        pro = ts.pro_api()
        try:
            df = pro.daily(trade_date=Date, fields='ts_code, close, pre_close')
            df.to_csv(fileName, mode='a', header=True)
        except:
            print(f'get yesterday stock fail!')

    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pre_close = row['pre_close']
            close = row['close']
            close = round(float(close), 2)
            if  close == round(float(pre_close) * 1.100, 2):
                listLimitStock.append(row['ts_code'])

    print(listLimitStock)

getLastTradeDate()


''''
下载分钟数据到本地csv文件函数：downloadMinutesToCsv
下载日线数据到本地csv文件函数：downloadDailyToCsv
'''
import tushare as ts
import pandas as pd
import csv
import time
import datetime
import os.path
import os

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')

#获得上一个交易日日期
def getLastTradeDate():
    date = time.strftime("%Y%m%d", time.localtime())
    #print(date)
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=date, end_date=date, fields = 'cal_date, pretrade_date')
    #print(df)
    #print(df.iloc[0,1])
    return df.iloc[0,1]

#获取所有股票,1)非深圳，上海股票剔除 2)ST股票剔除
def getAllStocks():
    listAllStocks = []
    stList = []
    date = str(time.strftime("%Y%m%d", time.localtime()))

    pro = ts.pro_api()
    try:
        df = pro.query('daily_basic', ts_code='', trade_date=date,fields='ts_code')
        for index, row in df.iterrows():
            if (True == row['ts_code'].startswith('00')) or (True == row['ts_code'].startswith('60')):
                listAllStocks.append(row['ts_code'])
    except Exception as e:
        print(f'getAllStocks daily basic failed!')
        return

    try:
        df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,fullname,enname')
    except Exception as e:
        print(f'getAllStocks stock basic failed!')
        return

    #保存ST股票，需要剔除
    for index, row in df.iterrows():
        if 'ST' in row['name']:
            stList.append(row['ts_code'])
    #把ST股票从保存的股票里面剔除
    listAllStocks = list(set(listAllStocks).difference(stList))

    tempList = []
    for key in listAllStocks:
        convertStock = convertStockId(key)
        tempList.append(convertStock)
    listAllStocks = tempList.copy()
    print(f'AllStocks num = {len(listAllStocks)}, ST: num={len(stList)}')

    return listAllStocks

#600333.SH --> sh600333
def convertStockId(s1):
    if s1.endswith('SH'):
        s1 = s1.replace('.SH', '')
        s1 = 'sh' + s1
    else:
        s1 = s1.replace('.SZ', '')
        s1 = 'sz' + s1
    return s1

#获取昨天涨停的股票
def getSurgedStocks():
    listSurged = []
    date = getLastTradeDate()
    pro = ts.pro_api()
    df = pro.limit_list(trade_date=date, limit_type='U', fields = 'ts_code, name')
    for index, row in df.iterrows():
        if (False == row['name'].startswith('*ST')):
            listSurged.append(row['ts_code'])
    print(f'Yesterday surged stock number = {len(listSurged)}')
    return listSurged

#获取收盘价 > 10日均线 1.05倍的黑名单
def getMa10BlackList(list1):
    ma10BlackList = []
    lastDate = getLastTradeDate()
    for key in list1:
        df = ts.pro_bar(ts_code=key, start_date='20200811', end_date=lastDate,ma=[10])
        for index, row in df.iterrows():
            close = row['close']
            ma10 = row['ma10']
            print(row['ma10'])
            #收盘价 > 10日均线 1.05倍
            if float(close) > (float(ma10) * 1.05):
                ma10BlackList.append(key)
            break
    return ma10BlackList

#getSurgedStocks()
startDate = '20200827'
endDate = '20190110'
g_dailyCsv = 'C:/python/csv/temp/mini/'
list1 = getAllStocks()
#print(list1)



''''
下载分钟数据到本地csv文件函数：downloadMinutesToCsv
下载日线数据到本地csv文件函数：downloadDailyToCsv
'''
import tushare as ts
import pandas as pd
import csv
import time
import datetime
#from datetime import datetime
import os.path
import os

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')

#保存从20100104到今天的可交易日期
def saveTradeCalendar():
    startDate = '20100104'
    now = datetime.datetime.now()
    endDate = now.strftime('%Y%m%d')

    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=startDate, end_date=endDate, is_open=1)
    readAndCheckCsv.deleteFile(g_calendarFile)
    df.to_csv(g_calendarFile, columns=['exchange','cal_date'])

#获得交易日
def getTradeCalendar(startDate, endDate):
    listTempCalendar = []
    listTradeCalendar = []
    startDate2010 = '20100104'
    now = datetime.datetime.now()
    currentDate = now.strftime('%Y%m%d')

    #获取从2010年到今天的可交易日期，并保存到一个列表里
    try:
        pro = ts.pro_api()
        df = pro.trade_cal(exchange='', start_date=startDate2010, end_date=currentDate, is_open=1, fields='cal_date')
    except Exception as e:
        print(f'get calendar failed, e={str(e)}')
        return
    listTempCalendar = list(df.cal_date)

    if 0 == len(listTempCalendar):
        print(f'日期文件不存在!')
        exit(0)

    begin_date = datetime.datetime.strptime(startDate, "%Y%m%d")
    calendarFileBeginDate = datetime.datetime.strptime(listTempCalendar[0], "%Y%m%d")
    if begin_date < calendarFileBeginDate:
        print(f'起始日期太早了，startDate = {startDate}, calendarFileBeginDate = {listTempCalendar[0]}')
        exit(0)

    end_date = datetime.datetime.strptime(endDate, "%Y%m%d")
    calendarFileEndDate = datetime.datetime.strptime(listTempCalendar[len(listTempCalendar)-1], "%Y%m%d")
    if end_date > calendarFileEndDate:
        print(f'结束日期太晚了，end_date = {end_date}, calendarFileEndDate = {listTempCalendar[len(listTempCalendar)-1]}')
        exit(0)

    startDataFlag = False
    endDateFlag = False
    if (startDate not in listTempCalendar) or (endDate not in listTempCalendar):
        begin_date = datetime.datetime.strptime(startDate, "%Y%m%d")
        end_date   = datetime.datetime.strptime(endDate, "%Y%m%d")
        if startDate in listTempCalendar:
            startDataFlag = True
        if endDate in listTempCalendar:
            endDateFlag = True
        for i in range(12):
            if False == startDataFlag:
                delta = datetime.timedelta(days=1)
                begin_date = begin_date + delta
                tempDate = str(begin_date.date())
                tempDate = tempDate.replace('-', '')
                if tempDate in listTempCalendar:
                    startDate = tempDate
                    startDataFlag = True

            if False == endDateFlag:
                delta = datetime.timedelta(days=-1)
                end_date = end_date + delta
                tempDate = str(end_date.date())
                tempDate = tempDate.replace('-', '')
                if tempDate in listTempCalendar:
                    endDate = tempDate
                    endDateFlag = True

    i = listTempCalendar.index(startDate)
    j = listTempCalendar.index(endDate)
    listTradeCalendar = listTempCalendar[i:(j+1)]

    return startDate, endDate, listTradeCalendar

#获取所有股票,1)非深圳，上海股票剔除 2)ST股票剔除
def getAllStocks(startDate, endDate):
    listAllStocks = []
    filterList = []
    stList = []

    pro = ts.pro_api()
    try:
        df = pro.query('daily_basic', ts_code='', trade_date=startDate,fields='ts_code, close, circ_mv')
    except Exception as e:
        print(f'getAllStocks daily basic failed!')
        return

    #1.1 保存非00/60开头的股票，其他需要剔除
    for index, row in df.iterrows():
        if (False == row['ts_code'].startswith('00')) and (False == row['ts_code'].startswith('60')) :
            filterList.append(index)

    #1.2 剔除非00/60开头的股票
    for i in range(len(filterList)):
        df = df.drop([filterList[i]])
    #全部股票保存到list
    for i in range(len(df)):
        listAllStocks.append(df.iloc[i,0])

    try:
        df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,fullname,enname')
    except Exception as e:
        print(f'getAllStocks stock basic failed!')
        return

    #2.1 保存ST股票，需要剔除
    for index, row in df.iterrows():
        if 'ST' in row['name']:
            stList.append(row['ts_code'])
    #2.2把ST股票从保存的股票里面剔除
    listAllStocks = list(set(listAllStocks).difference(stList))

    print(f'AllStocks num = {len(listAllStocks)}, No 00_60_prefix: num={len(filterList)}, ST: num={len(stList)}')
    print('getAllStocks: ' + str(listAllStocks))
    return listAllStocks

#下载日线数据，startDate = '20190202', endDate = '20200818', filePaht = 'C:/python/csv/zhangting/daily/2019to2020/'
def downloadDailyToCsv(startDate, endDate, filePath):
    startDate, endDate, listTradeCalendar = getTradeCalendar(startDate, endDate)
    listAllStocks = getAllStocks(startDate, endDate)

    for i in range(len(listAllStocks)):
        fileName = filePath + listAllStocks[i] + '.csv'

        if True == os.path.isfile(fileName):
            os.remove(name)

        pro = ts.pro_api()
        try:
            df = pro.query('daily', ts_code=listAllStocks[i], start_date=startDate, end_date=endDate)
        except:
            print(f'skip stock={listAllStocks[i]}')
            continue
        df = df.sort_index(ascending=False)
        df.to_csv(fileName, mode='a', header=True, columns=['trade_date', 'open', 'high', 'low', 'close', 'pre_close'])

def convertDate(date):
    str_list = list(date)
    str_list.insert(4, '-')
    str_list.insert(7, '-')
    dateStr = ''.join(str_list)
    return dateStr

#下载分钟数据到本地csv文件
def downloadMinutesToCsv(startDate, endDate, filePath):
    listStartCanlender = []
    listEndCanlender = []
    startTime = convertDate(startDate)
    endTime = convertDate(endDate)
    startTime = startTime + ' 09:30:00'
    endTime = endTime + ' 15:00:00'

    startDate, endDate, listTradeCalendar = getTradeCalendar(startDate, endDate)
    listAllStocks = getAllStocks(startDate, endDate)

    for i in range(len(listAllStocks)): #轮询所有股票
        fileName = filePath + listAllStocks[i] + '.csv'

        if True == os.path.isfile(fileName):
            os.remove(name)

        df = ts.pro_bar(ts_code=listAllStocks[i], freq='1min', start_date=startTime, end_date=endTime)
        df = df.sort_index(ascending=False)
        df.to_csv(fileName, mode='a', header=True, columns=['ts_code', 'trade_time', 'open', 'close', 'high', 'low'])

startDate = '20190101'
endDate = '20190110'
g_dailyCsv = 'C:/python/csv/temp/mini/'

#downloadDailyToCsv(startDate, endDate, g_dailyCsv) #把日线数据下载到本地
downloadMinutesToCsv(startDate, endDate, g_dailyCsv) #把分钟数据下载到本地
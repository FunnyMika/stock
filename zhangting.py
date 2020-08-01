import tushare as ts
import pandas as pd
import csv
import time
from datetime import datetime
import os.path
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#from readAndCheckCsv import saveProfitToCsv
#from readAndCheckCsv import drawProfitPic
import sys
import threading
import pymysql
import readAndCheckCsv

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')
g_listAllStocks = []
g_listSuspendStocks = []
g_listTradeCanlendar = []
g_listSingleStockMinHigh = []
g_listWhite = []
g_dicBuyStock = {}
g_dicYield = {}
g_totalCost = 1000000  #拿100万人民币进行测试
g_singlCost = 100000  #每支股票买10万块钱
g_limitPrice = 100.00 #股价超过100块钱则不买

filePathNewAllStock = 'C:/python/csv/zhangting/allStocks.csv'
g_whiteCsvFile = 'C:/python/csv/zhangting/whitelist.csv'
g_dbZhangTing = 'stockZT'
g_loopStockNum = 0
#获得交易日
def getTradeCanlendar(startDate, endDate):
    global g_listTradeCanlendar
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=startDate, end_date=endDate, is_open = 1)
    for i in range(len(df)):
        g_listTradeCanlendar.append(df.iloc[i,1])
    print('getTradeCanlendar: ' + str(g_listTradeCanlendar))

def readWhiteListFromCsv():
    global g_listWhite
    g_listWhite = []

    try:
        with open(g_whiteCsvFile, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_code = row['ts_code']
                g_listWhite.append(ts_code)
    except Exception as e:
        g_listWhite = []
    print(f'whiteList count={len(g_listWhite)}')
    print(g_listWhite)

#获取所有股票,1)非深圳，上海，创业板3类股票剔除 2)ST股票剔除 3)收盘价>100剔除
def getAllStocks(startDate, endDate):
    global g_listAllStocks
    filterList = []
    stList = []
    highPriceList = []
    whiteList = []

    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code='', trade_date=startDate,fields='ts_code, close, circ_mv')

    #1.1 保存非00/30/60开头的股票，需要剔除
    for index, row in df.iterrows():
        if (False == row['ts_code'].startswith('00')) and (False == row['ts_code'].startswith('30')) and (False == row['ts_code'].startswith('60')) or\
                (float(row['circ_mv']) > 1000000):
            filterList.append(index)

    #1.2 剔除非00/30/60开头的股票和市值超过100亿的
    for i in range(len(filterList)):
        df = df.drop([filterList[i]])
    #全部股票保存到list
    for i in range(len(df)):
        g_listAllStocks.append(df.iloc[i,0])

    df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,fullname,enname')
    #2.1 保存ST股票，需要剔除
    for index, row in df.iterrows():
        if 'ST' in row['name']:
            stList.append(row['ts_code'])
    #2.2把ST股票从保存的股票里面剔除
    for i in range(len(stList)):
        if stList[i] in g_listAllStocks:
            g_listAllStocks.remove(stList[i])

    #3.1 获取 价格 > 100的股票列表
    highPriceList = []
    df = pro.query('daily_basic', ts_code='', trade_date=endDate, fields='ts_code, close')
    for index, row in df.iterrows():
        if float(row['close']) > g_limitPrice:
             highPriceList.append(row['ts_code'])
    #3.2 把 价格 > 100 的股票从保存的股票里面剔除
    for i in range(len(highPriceList)):
        if highPriceList[i] in g_listAllStocks:
            g_listAllStocks.remove(highPriceList[i])

    #读取白名单列表 g_listWhite
    #readWhiteListFromCsv()

    #所有股票必须在白名单里才行
    '''tempAllList = []
    tempAllList = g_listAllStocks
    print(f'len = {len(tempAllList)}')
    i = 0
    for i in range(len(tempAllList)):
        code = tempAllList[i]
        code = code[0:6]
        if code not in g_listWhite:
            g_listAllStocks.remove(tempAllList[i])
    print(f'len2 = {len(g_listAllStocks)}')'''

    print(f'AllStocks num = {len(g_listAllStocks)}, No 00_30_60_prefix and > 市值100亿: num={len(filterList)}, ST: num={len(stList)}, price > 100: num={len(highPriceList)}')
    print('getAllStocks: ' + str(g_listAllStocks))

#获取某一天所有停牌的股票代码
def getSuspendStocks(date):
    global g_listSuspendStocks

    pro = ts.pro_api()
    df = pro.suspend_d(suspend_type='S', trade_date=date)
    for index, row in df.iterrows():
            g_listSuspendStocks.append(row['ts_code'])

#获取股票1分钟数据
#ts_code           trade_time            open  close   high    low     vol
#600000.SH         2020-01-08 09:31:00   12.41  12.44  12.45  12.41  880140
def getSingleStockMinInfo(ts_code, date):
    global g_listSingleStockMinHigh
    str_list = list(date)
    str_list.insert(4, '-')
    str_list.insert(7, '-')
    dateStr = ''.join(str_list)
    startDate = dateStr + ' 09:31:00'
    endDate = dateStr + ' 10:00:00'
    df = ts.pro_bar(ts_code=ts_code, freq='1min', start_date=startDate, end_date=endDate)
    #df.sort_index(axis=1,ascending=False)
    for i in range(len(df)):
        g_listSingleStockMinHigh.append(df.iloc[i, 4])
        #print(df.iloc[i, 1] + '   ' + str(df.iloc[i, 4])) #返回的时间顺序是从10:00 --> 9:31
    g_listSingleStockMinHigh.reverse() #重新排序，按照时间先后顺序排序，从9:31 --> 10：00

#计算涨停价，涨停价 = 昨日收盘价 * 1.100 (四舍五入，取小数点2位)
def calculateZhangTingPrice(price):
    highestPrice = round(float(price) * 1.100, 2)
    #print(f'calculateZhangtingPrice: price={price}, highestPrice={highestPrice}')
    return highestPrice

#获取某个股票某天的前一日收盘价
def getYesterdayClosePrice(ts_code, date):
    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code=ts_code, trade_date=date,fields='close')
    close = df.iloc[0,0] #第0行第0列
    print(f'getYesterdayClosePrice: ts_code = {ts_code}, date = {date}, closePrice = {close}')
    return float(close)

#获得某一天内某个股票的最高价和收盘价,open, high, close
def getOnedayHighestAndClosePrice(date, ts_code):
    openPrice, closePrice, highPrice = 0.0, 0.0, 0.0
    openFlag = False
    fileName = 'C:/python/csv/zhangting/20200106to20200717/' + ts_code + '.csv'
    date = convertDate(date)

    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if date in row['trade_time']:
                if False == openFlag:
                    openPrice = float(row['open'])
                    openFlag = True
                closePrice = float(row['close'])
                if highPrice < float(row['high']):
                    highPrice = float(row['high'])
    return openPrice, highPrice, closePrice

#计算收益率
def calculateYield(date):
    global g_dicYield
    #g_dicBuyStock = {'002500.SZ':'7.99'}  #临时测试使用
    if 0 == len(g_dicBuyStock):
        return
    try:
        for stock, value in g_dicBuyStock.items():
            open, high, close = getOnedayHighestAndClosePrice(date, stock)
            if open > (float(value) * 1.07): #开盘价>7%，以开盘价作为卖价
                yeild = int( ( (open - float(value)) / float(value) ) * 100 )
            elif (open < (float(value) * 1.07)) and (high > (float(value) * 1.07)):#开盘价<7%,  盘中>7% ，以7%卖出
                yeild = 7
            else: #否者当天收盘价为卖价
                yeild = int( ( (close - float(value)) / float(value) ) * 100 )
            #g_listYield.append(str(yeild))
            print(f'卖出：date={date}, code={stock}, yeild={yeild}')
            readAndCheckCsv.saveProfitToCsv(stock, date, yeild)
    except Exception as e:
        PASS

def convertDate(date):
    str_list = list(date)
    str_list.insert(4, '-')
    str_list.insert(7, '-')
    dateStr = ''.join(str_list)
    return dateStr

def saveMinuteDataInfo(ts_code, startDate, endDate):
    fileName = 'C:/python/csv/zhangting/' + ts_code +'.csv'
    startTime = convertDate(startDate)
    endTime   = convertDate(endDate)
    startTime = startTime + ' 09:30:00'
    endTime   = endTime + ' 15:00:00'

    df = ts.pro_bar(ts_code=ts_code, freq='1min', start_date=startTime, end_date=endTime)
    df = df.sort_index(ascending=False)
    if False == os.path.isfile(fileName):
        df.to_csv(fileName,mode='a', header=True,columns=['ts_code', 'trade_time', 'open', 'close', 'high'])
    else:
        df.to_csv(fileName, mode='a', header=False,columns=['ts_code', 'trade_time', 'open', 'close', 'high'])

def downloadMinutesToCsv(startDate, endDate):
    listStartCanlender = []
    listEndCanlender = []
    getTradeCanlendar(startDate, endDate)
    getAllStocks(startDate, endDate)  # 获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票

    # 1. 轮询所有日期，把第一个月的第一天取出来放到一个list里面
    for i in range(len(g_listTradeCanlendar)-1):
        tmpStr5 = g_listTradeCanlendar[i][0:6]
        tmpListStr = ''.join(listStartCanlender)
        if tmpStr5 not in tmpListStr:
            listStartCanlender.append(g_listTradeCanlendar[i])

    #1.轮询所有日期，把第一个月的最后一天取出来放到一个list里面
    g_listTradeCanlendar.sort(reverse=True)
    for i in range(len(g_listTradeCanlendar)-1):
        tmpStr5 = g_listTradeCanlendar[i][0:6]
        tmpListStr = ''.join(listEndCanlender)
        if tmpStr5 not in tmpListStr:
            listEndCanlender.append(g_listTradeCanlendar[i])
    listEndCanlender.sort(reverse=False)

    print(listStartCanlender)
    print(listEndCanlender)

    g_listTradeCanlendar.sort(reverse=False)

    for i in range(len(g_listAllStocks)): #轮询所有股票
        #2. 把每个月的分时数据取出来存入文件，有几个月就存几次文件
        print(f'Save stock: {g_listAllStocks[i]}')
        for j in range(len(listStartCanlender)):
            startDate = listStartCanlender[j]
            endDate   = listEndCanlender[j]
            try:
                saveMinuteDataInfo(g_listAllStocks[i], startDate, endDate)
            except Exception as e:
                continue

        # 3. 把每个文件里10点以后的数据删除

#从csv文件里读取某一个股票的某一天在某一时间段内，估计不超过g_limitPrice的数据，并保存到list里面返回
def getOneStockDataFromCsv(ts_code, date, skipTime):
    fileName = 'C:/python/csv/zhangting/20200106to20200717/' + ts_code + '.csv'
    lastTradeTime, lastClose, lastHigh, close, high = 0, 0, 0, 0, 0
    tradeTime = ''
    lastAddFlag = False
    qtClose, ztClose =0,0 #前天收盘价，昨天收盘价
    listClose150000 = []      #15:00:00收盘价
    listData = []
    date = convertDate(date)

    try:
        with open(fileName, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tradeTime = row['trade_time']
                close = row['close']
                high = row['high']
                if '15:00:00' in tradeTime:
                    listClose150000.append(tradeTime)
                    listClose150000.append(close)
                    listClose150000.append(high)

                if date in tradeTime:
                    if skipTime in tradeTime:
                        break
                    if False == lastAddFlag: #昨日收盘价保存在list第一条记录里
                        close150000Len = len(listClose150000)
                        if close150000Len < 6:
                            listData = []
                            break
                        listData.append(listClose150000[close150000Len - 1 - 5])
                        listData.append(listClose150000[close150000Len - 1 - 4])
                        listData.append(listClose150000[close150000Len - 1 - 3])
                        listData.append(listClose150000[close150000Len - 1 - 2])
                        listData.append(listClose150000[close150000Len - 1 - 1])
                        listData.append(listClose150000[close150000Len - 1 - 0])
                        lastAddFlag = True
                    listData.append(tradeTime)
                    listData.append(close)
                    listData.append(high)
                lastTradeTime = tradeTime
                lastClose = close
                lastHigh = high
    except Exception as e:
        listData = []
    #print(listData)
    return listData

#读取某一天所有股票的数据，把某一时间段内的数据保存在一个字典里，ts_code作为key，某一个股票的数据作为value
def getCurrentDayDataFromCsv(date, skipTime):
    allStockInfo = {}
    oneStockInfo = []
    for k in range(g_loopStockNum):#range(len(g_listWhite)):#range(len(g_listAllStocks)):
        oneStockInfo = []
        oneStockInfo = getOneStockDataFromCsv(g_listAllStocks[k], date, skipTime)
        if len(oneStockInfo):
            allStockInfo[g_listAllStocks[k]] = oneStockInfo
    #print(oneStockInfo)
    return allStockInfo

def mainFunc(startDate, endDate, endTime):
    global g_dicBuyStock
    global g_totalCost
    global g_singlCost
    global g_limitPrice
    global g_listTradeCanlendar
    global g_listAllStocks
    global g_loopStockNum

    skipStockList = []

    #startDate = '20200703'
    #endDate   = '20200708'
    hasReachMaxBoughtNum = False
    maxBoughtNum = 7

    # {'000001.SZ': ['2020-07-13 15:00:00', '14.89', '14.89', '2020-07-14 09:30:00', '14.9', '14.9', '2020-07-14 09:31:00', '14.86', '14.9', '2020-07-14 09:32:00'
    #保存某只股票10点前的分时数据，其中第一条记录是昨天的收盘价
    dictOneDayInfoTo10 = {}
    readAndCheckCsv.deleteProfitToCsv(readAndCheckCsv.g_profitFileName)

    #getAllStocks(startDate,endDate)  #获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票
    readWhiteListFromCsv()
    g_listAllStocks = g_listWhite
    #g_listAllStocks = ['000839.SZ']
    g_loopStockNum = len(g_listAllStocks)
    #g_loopStockNum = 1
    getTradeCanlendar(startDate, endDate) #获得起始日期内的合理交易日

    startTime = datetime.strptime('2020-01-01 09:30:00', '%Y-%m-%d %H:%M:%S')
    lastTime = datetime.strptime('2019-01-01 '+endTime, '%Y-%m-%d %H:%M:%S')
    delta = lastTime - startTime
    loopMin = int(delta.seconds / 60)

    #轮询所有交易日
    for i in range(0, len(g_listTradeCanlendar)):
        date = g_listTradeCanlendar[i]
        hasReachMaxBoughtNum = False
        skipStockList = []
        print(f'交易日期：{date}')

        #卖出昨天买入的股票
        calculateYield(date) #和昨天比较，计算收益率
        g_dicBuyStock = {}

        #if endDate in g_listTradeCanlendar

        #获取当天不停牌的所有股票在9:30--10:00之间的数据
        dictOneDayInfoTo10 = getCurrentDayDataFromCsv(date, endTime)
        if 0 == len(dictOneDayInfoTo10):
            continue

        startMin = 2
        for j in range(startMin, loopMin):  # 轮序从9:32--10:00之间的所有股票，每分钟轮序一次所有股票，看是否符合条件买入
            # 当日购买的股票数量达到上限就不再买入，跳过当前日期
            if True == hasReachMaxBoughtNum:
                break

            for keyCode in dictOneDayInfoTo10:
                #当日购买的股票数量达到上限就不再买入
                if True == hasReachMaxBoughtNum:
                    break

                #如果这个股票在当日已经买过，就不再买，继续寻找下一个股票
                if (keyCode in g_dicBuyStock) or (keyCode in skipStockList):
                    continue

                try:  # 获得当前股票的昨日收盘价
                    oldOldPrice = float(dictOneDayInfoTo10[keyCode][1])
                    oldPrice = float(dictOneDayInfoTo10[keyCode][4])
                except Exception as e:  # 如果股票今天才上市，那么昨天就没有数据，需要跳过
                    continue

                #如果不是首板也就是昨天涨停了，就跳过
                if oldPrice == calculateZhangTingPrice(oldOldPrice):
                    skipStockList.append(keyCode)
                    break

                #前4分钟如果有涨停价，就跳过这只股票
                skipFlag = False
                highestPrice = calculateZhangTingPrice(oldPrice)  # 计算出涨停价
                for loop in range(0, startMin):
                    tmpPrice = float(dictOneDayInfoTo10[keyCode][3*loop+7])
                    if tmpPrice == highestPrice: #根据收盘价计算
                        skipFlag = True
                        skipStockList.append(keyCode)
                        break
                if True == skipFlag:
                    continue

                # 获取当前时刻的收盘价
                currentClosePrice = float(dictOneDayInfoTo10[keyCode][3*j+8]) #根据最高价计算

                # 9:34--10:00之间，最高价能否达到涨停价，如果达到则保存返回，继续找下一个股票
                if float(currentClosePrice) == float(highestPrice):
                    g_dicBuyStock[keyCode] = str(highestPrice)
                    time1 = dictOneDayInfoTo10[keyCode][3*j+6]
                    print(f'买入：time={time1}, code={keyCode}, price={str(g_dicBuyStock[keyCode])}')
                    if len(g_dicBuyStock) >= maxBoughtNum:
                        hasReachMaxBoughtNum = True
    readAndCheckCsv.calculateProfit(readAndCheckCsv.g_profitFileName)
    readAndCheckCsv.drawProfitPic() #打印 startDate~~~~endDate 收益率

#calculateYield('20200717')
#getOnedayHighestAndClosePrice('20200717', '002500.SZ')
#runMain()
#getYesterdayClosePrice('002500.SZ', '20200717')
#getHighestPrice(6.23)
#getAllStocks()
#getSuspendStocks('20200618')
#getSingleStockMinInfo('002500.SZ', '20200717')

if __name__ == "__main__":
    localtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f'Start at {localtime}')

    startDate = '20200701'
    endDate = '20200707'
    endTime = '11:30:00'

    mainFunc(startDate, endDate, endTime)
    #getAllStocks(startDate, endDate)

    localtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f'End at {localtime}')

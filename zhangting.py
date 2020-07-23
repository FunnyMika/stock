import tushare as ts
import pandas as pd
import csv
import time
import os.path
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#from readAndCheckCsv import saveProfitToCsv
#from readAndCheckCsv import drawProfitPic

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')
g_listAllStocks = []
g_listSuspendStocks = []
g_listTradeCanlendar = []
g_listSingleStockMinHigh = []
g_dicFoundStock = {}
g_listYield = []
g_totalCost = 1000000  #拿100万人民币进行测试
g_singlCost = 100000  #每支股票买10万块钱
g_limitPrice = 100.00 #股价超过100块钱则不买

filePathNewAllStock = 'C:/python/csv/zhangting/allStocks.csv'

#获得交易日
def getTradeCanlendar(startDate, endDate):
    global g_listTradeCanlendar
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=startDate, end_date=endDate, is_open = 1)
    for i in range(len(df)):
        g_listTradeCanlendar.append(df.iloc[i,1])
    print('getTradeCanlendar: ' + str(g_listTradeCanlendar))

#获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票
def getAllStocks(startDate):
    global g_listAllStocks
    filterList = []
    pro = ts.pro_api()
    #df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,market,list_date')
    # df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,market,list_date')
    df = pro.query('daily_basic', ts_code='', trade_date=startDate,fields='ts_code')
    for index, row in df.iterrows():
        if (False == row['ts_code'].startswith('00')) and (False == row['ts_code'].startswith('30')) and (False == row['ts_code'].startswith('60')):
           # print('Filter stock:' + row['ts_code'])
            filterList.append(index)

    for i in range(len(filterList)):
        df = df.drop([filterList[i]])

    for i in range(len(df)):
        g_listAllStocks.append(df.iloc[i,0])

    print('getAllStocks: ' + str(g_listAllStocks))
    #df.to_csv(filePathNewAllStock,encoding='utf_8_sig')

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
    print(f'calculateZhangtingPrice: price={price}, highestPrice={highestPrice}')
    return highestPrice

#获取某个股票某天的前一日收盘价
def getYesterdayClosePrice(ts_code, date):
    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code=ts_code, trade_date=date,fields='close')
    close = df.iloc[0,0] #第0行第0列
    print(f'getYesterdayClosePrice: ts_code = {ts_code}, date = {date}, closePrice = {close}')
    return float(close)

#获得某一天内某个股票的最高价和收盘价
def getOnedayHighestAndClosePrice(date, stock):
    pro = ts.pro_api()
    df = pro.daily(ts_code=stock, trade_date=date, fields ='open, high, close')
    print(df)
    return df.iloc[0, 0], df.iloc[0, 1], df.iloc[0, 2]

#计算收益率
def calculateYield(date):
    global g_listYield
    #g_dicFoundStock = {'002500.SZ':'7.99'}  #临时测试使用
    if 0 == len(g_dicFoundStock):
        return
    for stock, value in g_dicFoundStock.items():
        open, high, close = getOnedayHighestAndClosePrice(date, stock)
        if open > (float(value) * 1.07): #开盘价>7%，以开盘价作为卖价
            yeild = int( ( (open - float(value)) / float(value) ) * 100 )
        elif (open < (float(value) * 1.07)) and (high > (float(value) * 1.07)):#开盘价<7%,  盘中>7% ，以7%卖出
            yeild = 7
        else: #否者当天收盘价为卖价
            yeild = int( ( (close - float(value)) / float(value) ) * 100 )
        g_listYield.append(str(yeild))
        print('calculateYield: ' + date + str(g_listYield))

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
    getAllStocks(startDate)  # 获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票

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
    lastTradeTime = 0
    lastClose = 0
    lastHigh = 0
    tradeTime = ''
    close = 0
    high = 0
    lastAddFlag = False
    listData = []

    str_list = list(date)
    str_list.insert(4, '-')
    str_list.insert(7, '-')
    date = ''.join(str_list)
    try:
        with open(fileName, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tradeTime = row['trade_time']
                close = row['close']
                high = row['high']
                if float(high) > float(g_limitPrice):
                    listData = []
                    break
                if date in tradeTime:
                    if skipTime in tradeTime:
                        break
                    if False == lastAddFlag:
                        listData.append(lastTradeTime)
                        listData.append(lastClose)
                        listData.append(lastHigh)
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
    for k in range(len(g_listAllStocks)):  # 轮询所有不停牌的股票
        if g_listAllStocks[k] not in g_listSuspendStocks:
            oneStockInfo = getOneStockDataFromCsv(g_listAllStocks[k], date, skipTime)
            if len(oneStockInfo):
                allStockInfo[g_listAllStocks[k]] = oneStockInfo
    #print(oneStockInfo)
    return oneStockInfo

def runMainUnuseful():
    global g_dicFoundStock

    startDate = '20200713'
    endDate   = '20200717'

    getAllStocks(startDate)  #获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票
    getTradeCanlendar(startDate, endDate) #获得起始日期内的合理交易日

    #轮询所有交易日
    for i in range(1,50):#range(1, len(g_listTradeCanlendar)):
        date = g_listTradeCanlendar[i]
        print(f'日期：{date}')

        calculateYield(date) #和昨天比较，计算收益率
        g_dicFoundStock = {}

        getSuspendStocks(date)  #获取当天的停牌股票信息
        for j in range(len(g_listAllStocks)): #轮询所有不停牌的股票
            if g_listAllStocks[j] not in g_listSuspendStocks:
                try: #获得当前股票的昨日收盘价
                    oldPrice = getYesterdayClosePrice(g_listAllStocks[j], g_listTradeCanlendar[i-1])
                except Exception as e: #如果股票今天才上市，那么昨天就没有数据，需要跳过
                    continue

                highestPrice = calculateZhangTingPrice(oldPrice) #计算出涨停价
                if int(highestPrice) > 150: #涨停价大于150，则返回继续找下一个股票
                    continue

                #获得某个股票9:31--10:00之间的分钟数据
                getSingleStockMinInfo(g_listAllStocks[j], date)

                # 开盘价为涨停价剔除, 继续找下一个股票
                if float(g_listSingleStockMinHigh[0]) == highestPrice:
                    continue

                #9:31--10:00之间，最高价能否达到涨停价，如果达到则保存返回，继续找下一个股票
                for k in range(1, len(g_listSingleStockMinHigh)):
                    if(float(g_listSingleStockMinHigh[k]) == highestPrice):
                        g_dicFoundStock[g_listAllStocks[j]] = str(highestPrice)
                        continue

    print(g_listYield) #打印 startDate~~~~endDate 收益率

def mainFunc():
    global g_dicFoundStock
    global g_totalCost
    global g_singlCost
    global g_limitPrice
    global g_listTradeCanlendar
    global g_listAllStocks

    startDate = '20200713'
    endDate   = '20200717'
    dictOneDayInfoTo10 = {}

    getAllStocks(startDate)  #获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票
    getTradeCanlendar(startDate, endDate) #获得起始日期内的合理交易日

    #轮询所有交易日
    for i in range(1, len(g_listTradeCanlendar)):
        date = g_listTradeCanlendar[i]
        print(f'交易日期：{date}')

        #卖出昨天买入的股票

        #calculateYield(date) #和昨天比较，计算收益率
        g_dicFoundStock = {}

        getSuspendStocks(date)  #获取当天的停牌股票信息

        #获取当天不停牌的所有股票在9:30--10:00之间的数据，而且股价小于g_limitPrice
        dictOneDayInfoTo10 = getCurrentDayDataFromCsv(date, '10:01:00')
        print(dictOneDayInfoTo10)
        return

        for j in range(1, 30): #轮序从9:31--10:00之间的所有股票，每分钟轮序一次所有股票，看是否符合条件买入
            for k in range(len(g_listAllStocks)): #轮询所有不停牌的股票
                if g_listAllStocks[k] not in g_listSuspendStocks:
                    #把当前股票数据读取list
                    #获取当前日期的前一天15:00:00的收盘价
                    try: #获得当前股票的昨日收盘价
                        oldPrice = getYesterdayClosePrice(g_listAllStocks[k], g_listTradeCanlendar[i-1])
                    except Exception as e: #如果股票今天才上市，那么昨天就没有数据，需要跳过
                        continue

                    highestPrice = calculateZhangTingPrice(oldPrice) #计算出涨停价
                    if int(highestPrice) > 150: #涨停价大于150，则返回继续找下一个股票
                        continue

                    #获得某个股票9:31--10:00之间的分钟数据
                    getSingleStockMinInfo(g_listAllStocks[k], date)

                    # 开盘价为涨停价剔除, 继续找下一个股票
                    if float(g_listSingleStockMinHigh[0]) == highestPrice:
                        continue

                    #9:31--10:00之间，最高价能否达到涨停价，如果达到则保存返回，继续找下一个股票
                    for k in range(1, len(g_listSingleStockMinHigh)):
                        if(float(g_listSingleStockMinHigh[k]) == highestPrice):
                            g_dicFoundStock[g_listAllStocks[k]] = str(highestPrice)
                            continue

    print(g_listYield) #打印 startDate~~~~endDate 收益率

#calculateYield('20200717')
#getOnedayHighestAndClosePrice('20200717', '002500.SZ')
#runMain()
#getYesterdayClosePrice('002500.SZ', '20200717')
#getHighestPrice(6.23)
#getAllStocks()
#getSuspendStocks('20200618')
#getSingleStockMinInfo('002500.SZ', '20200717')

if __name__ == "__main__":
    mainFunc()
    #downloadMinutesToCsv('20200106', '20200717')
    #getMinuteDataInfo('000002.SZ', '20140106', '20140306')
    #getOneStockDataFromCsv('000008.SZ','2020-01-07', '10:01:00')

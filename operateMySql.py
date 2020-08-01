import pymysql

def createDB(dbName):
    db = pymysql.connect(host='localhost',user='root', password='')
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    sql = 'CREATE DATABASE ' + dbName + ' DEFAULT CHARACTER SET utf8'
    cursor.execute(sql)
    db.close

def createTable(dbName, tableName):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
    cursor = db.cursor()
    #sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, ts_code VARCHAR(10) NOT NULL, trade_time VARCHAR(30) NOT NULL, open INT NOT NULL, close INT NOT NULL, high INT NOT NULL, PRIMARY KEY(id)'
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS %s" %tableName)
    # 使用预处理语句创建表
    sql = """CREATE TABLE %s (
             ts_code  CHAR(10) NOT NULL,
             trade_time  CHAR(25),
             open FLOAT,  
             close FLOAT,
             high FLOAT)""" %tableName
    cursor.execute(sql)
    db.close()

def insertDataToTable(dbName, tableName, listValue):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
    cursor = db.cursor()
    sql = 'INSERT INTO %s' %tableName + '(ts_code, trade_time, open, close, high) VALUES (%s,%s,%s,%s,%s)'
    try:
        if(len(listValue) > 1):
            cursor.executemany(sql, listValue)
        elif(1 == len(listValue)):
            cursor.execute(sql, listValue)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()

def deleteDataFromTable(dbName, tableName):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
    cursor = db.cursor()
    age = 24
    sql = 'DELETE FROM %s WHERE AGE > %s' % (tableName, age)
    cursor.execute(sql)
    db.commit()
    db.close()

def dropTable(dbName, tableName):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
    cursor = db.cursor()
    sql = 'DROP TABLE %s'%tableName
    cursor.execute(sql)
    db.close()

def printTableContent(dbName, tableName):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
    cursor = db.cursor()
    sql = "SELECT * FROM %s" %tableName
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            ts_code = row[0]
            trade_time = row[1]
            open = row[2]
            close = row[3]
            high = row[4]
            # 打印结果
            print("ts_code=%s,trade_time=%s,open=%s,close=%s,high=%s" % \
                  (ts_code, trade_time, open, close, high))
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()


dbName = 'stockZT'
tableName = 'a000001'
listValue = [('000001.SZ', '2020-06-01 09:30:00', 2.3, 2.4, 2.35)]
#createDB(dbName)
#createTable(dbName, tableName)
#insertDataToTable(dbName, tableName,listValue)
#deleteDataFromTable(dbName, tableName)
#dropTable(dbName, tableName)
#printTableContent(dbName, tableName)

#move from main.py
def getOneStockDataFromDB(ts_code, date, skipTime, dbName):
    fileName = 'C:/python/csv/zhangting/20200106to20200717/' + ts_code + '.csv'
    lastTradeTime = 0
    lastClose = 0
    lastHigh = 0
    tradeTime = ''
    close = 0
    high = 0
    lastAddFlag = False
    listData = []

    date = convertDate(date)

    try:
        db = pymysql.connect(host='localhost', user='root', password='', port=3306, db=dbName)
        cursor = db.cursor()
        tableName = convertTscodeToDbtable(ts_code)
        sql = "SELECT * FROM %s" % tableName
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                #ts_code = row[0]
                #trade_time = row[1]
                #open = row[2]
                #close = row[3]
                #high = row[4]
                tradeTime = row[1]
                close = row[3]
                high = row[4]
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
    except Exception as e:
        listData = []
    return listData

def getCurrentDayDataFromDB(date, skipTime):
    allStockInfo = {}
    oneStockInfo = []
    count = 0
    for k in range(len(g_listAllStocks)):  # 轮询所有不停牌的股票
        #if g_listAllStocks[k] not in g_listSuspendStocks:
        oneStockInfo = []
        oneStockInfo = getOneStockDataFromDB(g_listAllStocks[k], date, skipTime, g_dbZhangTing)
        if len(oneStockInfo):
            allStockInfo[g_listAllStocks[k]] = oneStockInfo
            count += 1
            #print(f'count={count}' + ', ' + date+ ':  stock=' + g_listAllStocks[k])
            if count > 100:
                break
            #print(oneStockInfo)
    #print(oneStockInfo)
    return allStockInfo

def convertTscodeToDbtable(ts_code):
    preName = 'stock'
    temp = ts_code[0:6]
    return preName + temp

def insertOneStockToMySql(ts_code):
    fileName = 'C:/python/csv/zhangting/20200106to20200717/' + ts_code + '.csv'
    ts_code, tradeTime = '', ''
    openPrice, closePrice, highPrice = 0.0, 0.0, 0.0
    listValue = []
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts_code = row['ts_code']
            tradeTime = row['trade_time']
            openPrice = row['open']
            closePrice = row['close']
            highPrice = row['high']
            listValue.append((ts_code, tradeTime, openPrice, closePrice, highPrice))
    if(len(listValue) > 0):
        convertCode = convertTscodeToDbtable(ts_code)
        operateMySql.createTable(g_dbZhangTing, convertCode)
        operateMySql.insertDataToTable(g_dbZhangTing, convertCode, listValue)

def writeAllStockCsvToDb():
    startDate = '20200106'
    endDate = '20200717'

    getAllStocks(startDate, endDate)  # 获取所有股票,从所有股票里过滤出深圳，上海，创业板3类股票

    # 轮询所有股票
    for i in range(1, len(g_listAllStocks)):
        ts_code = g_listAllStocks[i]
        insertOneStockToMySql(ts_code)
        localtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'End store stock {ts_code} to DB, time = {localtime}')

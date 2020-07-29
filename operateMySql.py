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
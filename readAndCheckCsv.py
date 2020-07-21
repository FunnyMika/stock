import tushare as ts
import pandas as pd
import time
import csv

def readFile(ts_code):
    fileName = 'C:/python/csv/zhangting/20200106to20200717/' + ts_code + '.csv'
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if '15:00:00' in row['trade_time']:
                print(row['trade_time'] + ' ' +  str(row['close']))

readFile('000001.SZ')
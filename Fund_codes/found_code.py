import requests
import json
import re
import datetime
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import os
import warnings
warnings.filterwarnings('ignore')


# 浏览器头
headers = {'content-type': 'application/json; charset=utf-8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}

codes = ['161725', '005827', '003095', '003096']
# 获取表格对象
workbook = load_workbook('/Users/ayd/Desktop/基金数据买卖点.xlsx')
sheetnames = workbook.sheetnames
# 昨天日期
yesterday = datetime.date.today() + datetime.timedelta(-1)

for code in codes:
    url = "http://fundgz.1234567.com.cn/js/%s.js"%code
    # url = "http://fund.eastmoney.com/pingzhongdata/%s.js"%code
    
    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)
    data = json.loads(search[0])
    
    # 创建sheet
    if data['name'] not in sheetnames:
        workbook.create_sheet(data['name'])
    sheet = workbook[data['name']]
    
    # 数据写入
    sheet['A1'] = '基金代码：' + data['fundcode']
    sheet['A2'] = '交易日期'
    sheet['B2'] = '单位净值'
    # 判断日期再写入
    all_date = [sheet['A'][a].value for a in range(len(sheet['A']))][2:]
    if str(yesterday) not in all_date:
        # print('没有数据')
        sheet.insert_rows(idx=3, amount=1)
        sheet['A3'] = data['jzrq']
        sheet['B3'] = float(data['dwjz'])
        if len(sheet['A']) > 3:
            sheet['C3'] = float((sheet['B3'].value - sheet['B4'].value) / sheet['B4'].value * 100)

workbook.save('/Users/ayd/Desktop/基金数据买卖点.xlsx')
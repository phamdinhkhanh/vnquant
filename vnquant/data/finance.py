# Copyright (c) general_backbone. All rights reserved.
from bs4 import BeautifulSoup
import requests
import vnquant.utils.utils as utils
import pandas as pd
import logging as logging
import re
import requests
import time
import numpy as np
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class FinanceLoader():
    def __init__(self, symbol, start, end, *arg, **karg):
        self.symbol = symbol
        self.start = start
        self.end = end

    def get_finan_report(self):
        start_time = time.time()
        page = requests.get("https://finfo-api.vndirect.com.vn/v3/stocks/financialStatement?secCodes={}&reportTypes=QUARTER&modelTypes=1,89,101,411&fromDate={}&toDate={}".format(self.symbol, self.start, self.end))
        data = page.json()
        end_time = time.time()
        data_dates = {}
        #print('request time: ', end_time-start_time)
        start_time = time.time()
        for item in data['data']['hits']:
            item = item['_source']
            date = item['fiscalDate']
            itemName = item['itemName']
            itemCode = item['itemCode']
            numericValue = item['numericValue']
            if date not in data_dates:
                data_dates[date] = [[], []]
            else:
                if itemName not in data_dates[date][0]:
                    data_dates[date][0].append(itemName)
                    data_dates[date][1].append(numericValue)
        end_time = time.time()
        #print('access data time: ', end_time-start_time)
        start_time = time.time()
        for i, (date, item) in enumerate(data_dates.items()):
            df_date = pd.DataFrame(data={'index':item[0], date[:7]:item[1]})
            if i == 0:
                df = df_date
            else:
                df = pd.merge(df, df_date, how='inner')
        df.set_index('index', inplace=True)
        end_time = time.time()
        #print('merge time: ', end_time-start_time)
        return df

    def get_business_report(self):
        start_time = time.time()
        page = requests.get("https://finfo-api.vndirect.com.vn/v3/stocks/financialStatement?secCodes={}&reportTypes=QUARTER&modelTypes=2,90,102,412&fromDate={}&toDate={}".format(self.symbol, self.start, self.end))
        data = page.json()
        end_time = time.time()
        data_dates = {}
        #print('request time: ', end_time-start_time)
        start_time = time.time()
        for item in data['data']['hits']:
            item = item['_source']
            date = item['fiscalDate']
            itemName = item['itemName']
            itemCode = item['itemCode']
            numericValue = item['numericValue']
            if date not in data_dates:
                data_dates[date] = [[], []]
            else:
                if itemName not in data_dates[date][0]:
                    data_dates[date][0].append(itemName)
                    data_dates[date][1].append(numericValue)
        end_time = time.time()
        #print('access data time: ', end_time-start_time)
        start_time = time.time()
        for i, (date, item) in enumerate(data_dates.items()):
            df_date = pd.DataFrame(data={'index':item[0], date[:7]:item[1]})
            if i == 0:
                df = df_date
            else:
                df = pd.merge(df, df_date, how='inner')
        df.set_index('index', inplace=True)
        end_time = time.time()
        #print('merge time: ', end_time-start_time)
        return df

    def get_cashflow_report(self):
        start_time = time.time()
        page = requests.get("https://finfo-api.vndirect.com.vn/v3/stocks/financialStatement?secCodes={}&reportTypes=QUARTER&modelTypes=3,91,103,413&fromDate={}&toDate={}".format(self.symbol, self.start, self.end))
        data = page.json()
        end_time = time.time()
        data_dates = {}
        #print('request time: ', end_time-start_time)
        start_time = time.time()
        for item in data['data']['hits']:
            item = item['_source']
            date = item['fiscalDate']
            itemName = item['itemName']
            itemCode = item['itemCode']
            numericValue = item['numericValue']
            if date not in data_dates:
                data_dates[date] = [[], []]
            else:
                if itemName not in data_dates[date][0]:
                    data_dates[date][0].append(itemName)
                    data_dates[date][1].append(numericValue)
        end_time = time.time()
        #print('access data time: ', end_time-start_time)
        start_time = time.time()
        for i, (date, item) in enumerate(data_dates.items()):
            df_date = pd.DataFrame(data={'index':item[0], date[:7]:item[1]})
            if i == 0:
                df = df_date
            else:
                df = pd.merge(df, df_date, how='inner')
        df.set_index('index', inplace=True)
        end_time = time.time()
        #print('merge time: ', end_time-start_time)
        return df

    def get_basic_index(self):
        start_year = int(self.start[:4])
        end_year = int(self.end[:4])
        years = np.arange(start_year, end_year+1, 1)[::-1]
        years = ['{}-12-31'.format(year) for year in years]
        data_dates = {}
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        headers = {'User-Agent': user_agent}
        for year in years:
            page = requests.get("https://finfo-api.vndirect.com.vn/v4/ratios?q=code:{}~itemCode:53030,52005,51050,53021,52001,52002,54018,712010,712020,712030,712040~reportDate:{}".format(self.symbol, year), headers=headers)
            data = page.json()
            
            for item in data['data']:
                date = item['reportDate']
                itemName = item['itemName']
                itemCode = item['itemCode']
                value = item['value']
                if date not in data_dates:
                    data_dates[date] = [[], []]
                else:
                    if itemName not in data_dates[date][0] and itemName != "":
                        data_dates[date][0].append(itemName)
                        data_dates[date][1].append(value)

        for i, (date, item) in enumerate(data_dates.items()):
            df_date = pd.DataFrame(data={'index':item[0], date[:7]:item[1]})
            if i == 0:
                df = df_date
            else:
                df = pd.merge(df, df_date, how='inner')

        df.set_index('index', inplace=True)
        return df
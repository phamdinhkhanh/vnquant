# Copyright (c) vnquant. All rights reserved.
import pandas as pd
import requests
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
# sys.path.insert(0,'/Users/phamdinhkhanh/Documents/vnquant')
from vnquant import configs
from vnquant.data.loader.proto import DataLoadProto
from vnquant.log import logger
from vnquant.utils import utils

URL_VND = configs.URL_VND
API_VNDIRECT = configs.API_VNDIRECT
URL_CAFE = configs.URL_CAFE
HEADERS = configs.HEADERS
REGEX_PATTERN_PRICE_CHANGE_CAFE = configs.REGEX_PATTERN_PRICE_CHANGE_CAFE
STOCK_COLUMNS_CAFEF = configs.STOCK_COLUMNS_CAFEF
STOCK_COLUMNS_CAFEF_FINAL = configs.STOCK_COLUMNS_CAFEF_FINAL

class DataLoaderCAFE(DataLoadProto):
    def __init__(self, symbols, start, end, *arg, **karg):
        self.symbols = symbols
        self.start = start
        self.end = end
        super(DataLoaderCAFE, self).__init__(symbols, start, end)

    def download(self):
        stock_datas = []
        symbols = self.pre_process_symbols()
        logger.info('Start downloading data symbols {} from CAFEF, start: {}, end: {}!'.format(symbols, self.start, self.end))

        for symbol in symbols:
            stock_datas.append(self.download_one(symbol))

        data = pd.concat(stock_datas, axis=1)
        data = data.sort_index(ascending=False)
        return data

    def download_one(self, symbol):
        start_date = utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        end_date = utils.convert_text_dateformat(self.end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        params = {
            "Symbol": symbol, # symbol of stock
            "StartDate": start_date, # start date
            "EndDate": end_date, # end date
            "PageIndex": 1, # page number
            "PageSize":delta.days + 1 # the size of page
        }
        # Note: We set the size of page equal to the number of days from start_date and end_date
        # and page equal to 1, so that we can get a full data in the time interval from start_date and end_date
        res = requests.get(URL_CAFE, params=params)
        data = res.json()['Data']['Data']
        if not data:
            logger.error(f"Data of the symbol {symbol} is not available")
            return None
        data = pd.DataFrame(data)
        data[['code']] = symbol
        stock_data = data[['code', 'Ngay',
                           'GiaDongCua', 'GiaMoCua', 'GiaCaoNhat', 'GiaThapNhat', 'GiaDieuChinh', 'ThayDoi',
                           'KhoiLuongKhopLenh', 'GiaTriKhopLenh', 'KLThoaThuan', 'GtThoaThuan']].copy()

        stock_data.columns = STOCK_COLUMNS_CAFEF

        stock_change = stock_data['change_str'].str.extract(REGEX_PATTERN_PRICE_CHANGE_CAFE, expand=True)
        stock_change.columns = ['change', 'percent_change']
        stock_data = pd.concat([stock_data, stock_change], axis=1)
        stock_data = stock_data[STOCK_COLUMNS_CAFEF_FINAL]

        list_numeric_columns = [
            'close', 'open', 'high', 'low', 'adjust_price',
            'change', 'percent_change',
            'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile'
        ]
        
        stock_data = stock_data.set_index('date')
        stock_data[list_numeric_columns] = stock_data[list_numeric_columns].astype(float)
        stock_data.index = list(map(lambda x: datetime.strptime(x, '%d/%m/%Y'), stock_data.index))
        stock_data.index.name = 'date'
        stock_data = stock_data.sort_index(ascending=False)
        stock_data.fillna(method='ffill', inplace=True)
        stock_data['total_volume'] = stock_data.volume_match + stock_data.volume_reconcile
        stock_data['total_value'] = stock_data.value_match + stock_data.value_reconcile

        # Create multiple columns
        iterables = [stock_data.columns.tolist(), [symbol]]
        mulindex = pd.MultiIndex.from_product(iterables, names=['Attributes', 'Symbols'])
        stock_data.columns = mulindex

        logger.info('data {} from {} to {} have already cloned!' \
                     .format(symbol,
                             utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d'),
                             utils.convert_text_dateformat(self.end, origin_type='%d/%m/%Y', new_type='%Y-%m-%d')))
        return stock_data
    
# if __name__ == "__main__":  
#     loader2 = DataLoaderCAFE(symbols=["VND"], start="2017-01-10", end="2019-02-15")
#     print(loader2.download())

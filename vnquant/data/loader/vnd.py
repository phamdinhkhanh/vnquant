# Copyright (c) vnquant. All rights reserved.
from typing import Union, Optional
import pandas as pd
import requests
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
# sys.path.insert(0,'/Users/phamdinhkhanh/Documents/vnquant')
from vnquant import utils
from vnquant import configs
from vnquant.log import logger
from vnquant.data.loader.proto import DataLoadProto

API_VNDIRECT = configs.API_VNDIRECT
HEADERS = configs.HEADERS
class DataLoaderVND(DataLoadProto):
    def __init__(self, 
        symbols: list, 
        start: Optional[Union[str, datetime]], 
        end: Optional[Union[str, datetime]], *arg, **karg):
        self.symbols = symbols
        self.start = start
        self.end = end
        super().__init__(symbols, start, end)

    def download(self):
        stock_datas = []
        symbols = self.pre_process_symbols()
        logger.info('Start downloading data symbols {} from VNDIRECT, start: {}, end: {}!'.format(symbols, self.start, self.end))
        for symbol in symbols:
            stock_datas.append(self.download_one(symbol))
        data = pd.concat(stock_datas, axis=1)
        data = data.sort_index(ascending=False)
        return data

    def download_one(self, symbol):
        start_date = utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        end_date = utils.convert_text_dateformat(self.end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        query = 'code:' + symbol + '~date:gte:' + start_date + '~date:lte:' + end_date
        delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        params = {
            "sort": "date", # the field applied to sort values.
            "size": delta.days + 1, # size of a single page in pagination.
            "page": 1, # number of page to download.
            "q": query # code, start date and end date.
        }
        # Note: We set the size of page equal to the number of days from start_date and end_date
        # and page equal to 1, so that we can get a full data in the time interval from start_date and end_date
        res = requests.get(API_VNDIRECT, params=params, headers=HEADERS)
        data = res.json()['data']
        if not data:
            logger.error(f"Data of the symbol {symbol} is not available")
            return None
        data = pd.DataFrame(data)        
        stock_data = data[['code', 'date', 'floor',
                           'basicPrice', 'ceilingPrice', 'floorPrice',
                           'close', 'open', 'high', 'low', 'average', 
                           'adClose', 'adOpen', 'adHigh', 'adLow', 'adAverage', 
                           'change', 'adChange', 'pctChange',
                           'nmVolume', 'nmValue', 'ptVolume', 'ptValue']].copy()
        
        stock_data.columns = configs.STOCK_COLUMNS
        stock_data = stock_data.set_index('date')
        list_numeric_columns = [
            'basic_price', 'ceiling_price', 'floor_price',
            'close', 'open', 'high', 'low', 'average',
            'adjust_close', 'adjust_open', 'adjust_high', 'adjust_low', 'adjust_average',
            'change', 'adjust_change', 'percent_change',
            'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile'
        ]
        stock_data[list_numeric_columns] = stock_data[list_numeric_columns].astype(float)
        stock_data.index = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d'), stock_data.index))
        stock_data.index.name = 'date'
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
#     loader1 = DataLoaderVND(symbols=["VND"], start="2017-01-10", end="2019-02-15")
#     print(loader1.download())

# Copyright (c) vnquant. All rights reserved.
from typing import Union, Optional
import requests
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# import sys
# sys.path.insert(0, '/Users/phamdinhkhanh/Documents/vnquant')
import pandas as pd
from vnquant import configs
from vnquant.data.loader import DataLoaderVND, DataLoaderCAFE
from vnquant.log import logger


URL_VND = configs.URL_VND
API_VNDIRECT = configs.API_VNDIRECT
URL_CAFE = configs.URL_CAFE
HEADERS = configs.HEADERS

class DataLoader():
    '''
    The DataLoader class is designed to facilitate the downloading and structuring of stock data from different data sources. 
    It supports customization in terms of data sources, time frames, and data formatting.
    '''
    def __init__(self, 
        symbols: Union[str, list], 
        start: Optional[Union[str, datetime]]=None,
        end: Optional[Union[str, datetime]]=None, 
        data_source: str='CAFE', 
        minimal: bool=True,
        table_style: str='levels',
        *arg, **karg):
        '''
        Args:
            - symbols (Union[str, list]): A single stock symbol as a string or multiple stock symbols as a list of strings.
            - start (Optional[Union[str, datetime]], default=None): The start date for the data. Can be a string in the format 'YYYY-MM-DD' or a datetime object.
            - end (Optional[Union[str, datetime]], default=None): The end date for the data. Can be a string in the format 'YYYY-MM-DD' or a datetime object.
            - data_source (str, default='CAFE'): The data source to be used for downloading stock data. Currently supports 'CAFE' and 'VND'.
            - minimal (bool, default=True): If True, returns a minimal set of columns which are important. If False, returns all available columns.
            - table_style (str, default='levels'): The style of the returned table. Options are 'levels', 'prefix', and 'stack'.
        Return:
            - DataFrame: A pandas DataFrame containing the stock data with columns formatted according to the specified table_style.
        '''
        self.symbols = symbols
        self.start = start
        self.end = end
        self.data_source = data_source
        self.minimal = minimal
        self.table_style = table_style
    
    def download(self):
        if str.lower(self.data_source) == 'vnd':
            loader = DataLoaderVND(self.symbols, self.start, self.end)
            stock_data = loader.download()
        else:
            loader = DataLoaderCAFE(self.symbols, self.start, self.end)
            stock_data = loader.download()
        
        if self.minimal:
            if str.lower(self.data_source) == 'vnd':
                stock_data = stock_data[['code', 'high', 'low', 'open', 'close', 'adjust_close', 'volume_match', 'value_match']]
            else:
                stock_data = stock_data[['code', 'high', 'low', 'open', 'close', 'adjust_price', 'volume_match', 'value_match']]
            # Rename columns adjust_close or adjust_price to adjust
            list_columns_names = stock_data.columns.names
            list_tupple_names = stock_data.columns.values
            
            for i, (metric, symbol) in enumerate(list_tupple_names):
                if metric in ['adjust_price', 'adjust_close']:
                    list_tupple_names[i] = ('adjust', symbol)

            stock_data.columns = pd.MultiIndex.from_tuples(
                list_tupple_names,
                names=list_columns_names
            )
        if self.table_style == 'levels':
            return stock_data

        if self.table_style == 'prefix':
            new_column_names = [f'{symbol}_{attribute}' for attribute, symbol in stock_data.columns]
            stock_data.columns = new_column_names
            return stock_data

        if self.table_style == 'stack':
            stock_data = stock_data.stack('Symbols').reset_index().set_index('date')
            stock_data.pop('Symbols')
            new_columns = [col if col!='Symbols' else 'code' for col in list(stock_data.columns)]
            stock_data.columns = new_columns
            return stock_data
        

# ---------------------------------------------------------------------------
# project: vn_quant_update
# author: binh.truong
# date: 1st Jan 2023
# ---------------------------------------------------------------------------

import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz


class VND_OHLCV(object):
    """
    A class to visualize stock data.
    Data source: VNDIRECT API.
    REST API from candle stick chart OHLCV of each stock symbol in Vietnam stock market.
    """
    def __init__(
        self, symbol: str='FPT', 
        start_date=datetime.now(),
        end_date=datetime.now()-timedelta(days=7),
        ) -> None:
        """
        Class Attributes:
            symbol: (str) -> Stock symbol.
            resolution: (str) -> Time resolution, e.g., 1, D, W, M, Y.
            start_date: (datetime) -> Start date.
            end_date: (datetime) -> End date.
        """
        self.symbol = symbol
        # self.resolution = resolution
        self.start_date = start_date
        self.end_date = end_date
        self.VND_API = r'https://dchart-api.vndirect.com.vn/dchart/history'
        self.dataframe = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'dchart-api.vndirect.com.vn'
        }
        self.params = {
            'symbol': None,
            'resolution': None,
            'from': None,
            'to': None
        }
    

    def __str__(self) -> str:
        return f'''StockVisualization(
            symbol={self.symbol}, resolution={self.resolution}, 
            start_date={self.start_date}, end_date={self.end_date}
        )'''


    def set_params(self, params: dict) -> None:
        self.params = params


    def get_data(self, params) -> pd.DataFrame:
        """
        A function to get stock data from VNDIRECT API.
        The data will be open, high, low, close, volume, and date.
        ------------
        Args:
            params: dict -> API parametters
        Returns:
            data: (pd.DataFrame) -> A DataFrame containing stock data.
        """
        def _get_date_time_from_timestamp(timestamp):
            return datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Bangkok'))

        response = requests.get(self.VND_API, params=params, headers=self.header)
        data_json = response.json()
        data = pd.DataFrame(data_json)
        data['Date'] = data['t'].apply(lambda x: _get_date_time_from_timestamp(x))
        # Convert price columns
        columns_to_convert = ['o', 'c', 'h', 'l']
        for column in columns_to_convert:
            data[column] = data[column].astype(float) * 1000
        # data = data.set_index('datetime')
        data = data.drop(['t', 's'], axis=1)
        data.rename(
            columns = {
                'o':'open', 'c':'close',
                'h':'high', 'l': 'low', 
                'v': 'volume'
            }, 
            inplace = True
        )
        self.data_frame = data
        return self.data_frame
    


if __name__ == "__main__":
    df = VND_OHLCV('HPG', datetime.now(), datetime.now()-timedelta(days=5))
    params = {
        'symbol': 'VNM',
        'resolution': '1',
        'to': int(datetime.now().timestamp()),
        'from': int((datetime.now() - timedelta(days=365)).timestamp()),
    }
    data = df.get_data(params=params)
    print(data)


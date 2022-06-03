# Copyright (c) general_backbone. All rights reserved.
from vnquant.data import DataLoader
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vnquant.utils.utils as utils
import pandas as pd

def _vnquant_candle_stick_source(symbol,
                                 start_date, end_date,
                                 colors=['blue', 'red'],
                                 width=800, height=600,
                                 show_vol=True,
                                 data_source='VND',
                                 **kargs):
    loader = DataLoader(symbol, start_date, end_date, minimal=True, data_source=data_source)
    data = loader.download()
    symbol = list(data.columns.levels[1])[0]
    data.columns = ['high', 'low', 'open', 'close', 'adjust', 'volume']
    title = '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                        # subplot_titles=('Price', 'Volume'),
                        row_heights=[0.6, 0.4])

    fig.append_trace(go.Candlestick(
        x=data.index,
        open=data['open'], high=data['high'],
        low=data['low'], close=data['close'],
        increasing_line_color=colors[0],
        decreasing_line_color=colors[1]),
        row=1, col=1)

    if show_vol:
        fig.append_trace(go.Bar(
            x=data.index,
            y=data['volume'],
            name='Volume'),
            row=2, col=1)

    fig.update_layout(
        title=title,
        yaxis_title='Price',
        xaxis_title='Date',
        width=width,
        height=height,
        showlegend=False
    )

    fig.show()

def _vnquant_candle_stick(data,
                          title=None,
                          xlab='Date', ylab='Price',
                          start_date=None, end_date=None,
                          colors=['blue', 'red'],
                          width=800, height=600,
                          show_vol=True,
                          data_source='VND',
                          **kargs):
    '''
    :param data: is pandas data frame of OHLC type or OHLCV type, or string symbol of any VietNam stock index.
    in case symbol, data is automatically cloned from open source.
    :param title: General title of candle stick chart.
    :param xlab: y label
    :param ylab: y label
    :param start_date: start date
    :param end_date: end date
    :param colors: list colors according to increasing and decreasing color stick candle.
    :param width: with of plot frame. Default 800px
    :param height: height of plot frame. Default 600px
    :param show_vol: is show volume of stock price
    :param data_source: invalid when use symbol intead of data frame. Source to clone data, 'VND' or 'CAFE'.
    :param kargs:
    :return:
    '''
    # Download data from source
    if isinstance(data, str):
        _vnquant_candle_stick_source(symbol=data, start_date=start_date, end_date=end_date,
                                     colors=colors, width=width,
                                     height=height, show_vol=show_vol,
                                     data_source=data_source)
    else:
        if show_vol:
            assert utils._isOHLCV(data)
            defau_cols = ['high', 'low', 'open', 'close', 'volume']
            data = data[defau_cols].copy()
            data.columns = defau_cols
        else:
            assert utils._isOHLC(data)
            defau_cols = ['high', 'low', 'open', 'close']
            data = data[defau_cols].copy()
            data.columns = defau_cols

        x = data.index

        if not isinstance(x, pd.core.indexes.datetimes.DatetimeIndex):
            raise IndexError('index of dataframe must be DatetimeIndex!')

        if start_date is None:
            start_date = max(data.index)
        if end_date is None:
            end_date = max(data.index)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                            # subplot_titles=('Price', 'Volume'),
                            row_heights=[0.6, 0.4])

        fig.append_trace(go.Candlestick(
            x=x,
            open=data['open'], high=data['high'],
            low=data['low'], close=data['close'],
            increasing_line_color=colors[0],
            decreasing_line_color=colors[1]),
            row=1, col=1)

        if show_vol:
            fig.append_trace(go.Bar(
                x=x,
                y=data['volume'],
                name='Volume'),
                row=2, col=1)

        fig.update_layout(
            title=title,
            yaxis_title=xlab,
            xaxis_title=ylab,
            showlegend=False
        )

        fig.show()


# _vnquant_candle_stick_source('VND', '2019-09-01', '2019-11-01', show_vol=False)
# _vnquant_candle_stick(data_cafe, None, ylab, xlab, start_date = '2019-01-01', end_date='2019-05-31')
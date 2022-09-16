# Copyright (c) general_backbone. All rights reserved.
from vnquant.data import DataLoader
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vnquant.utils.utils as utils
import pandas as pd
import numpy as np

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

def vnquant_candle_stick_source(
        symbol,
        start_date, end_date,
        colors=['blue', 'red'],
        width=800, height=600,
        data_source='VND',
        show_advanced = ['volume', 'macd', 'rsi'],
        **kargs
    ):
    '''
    This function is to visualize a candle stick stock index with advanced metrics
    Args:
        symbol (string): stock index
        start_date (string: 'yyyy-mm-dd'): start date
        end_date (string: 'yyyy-mm-dd'): end date
        colors (list: ['blue', 'red']): list colors of up and down candle
        width (int: 800): width of graph figure
        height (int: 600): height of graph figure
        data_source (string: 'VND'): data source to get stock price
        show_advanced (list: ['volume', 'macd', 'rsi']): list of advanced stock index to show up.
        
    Example:
        from vnquant import plot as pl
        pl.vnquant_candle_stick_source(
            symbol='TCB',
            title='TCB symbol from 2022-01-01 to 2022-10-01',
            xlab='Date', ylab='Price',
            start_date='2022-01-01',
            end_date='2022-10-01',
            data_source='CAFE',
            show_advanced = ['volume', 'macd', 'rsi']
        )
    '''
    
    loader = DataLoader(symbol, start_date, end_date, minimal=True, data_source=data_source)
    data = loader.download()
    symbol = list(data.columns.levels[1])[0]
    data.columns = ['high', 'low', 'open', 'close', 'adjust', 'volume']
    title = '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date)
    num_indices = len(show_advanced)

    if num_indices == 3:
        r_price = 1
        r_volume = 2
        r_macd = 3
        r_rsi = 4
        w_macd = 1
        w_rsi = 1
        row_heights = [0.3, 0.3, 0.15, 0.15]

    if 'macd' not in show_advanced:
        r_price = 1
        r_volume = 2
        r_rsi = 3
        w_rsi = 1
        row_heights = [0.5, 0.3, 0.2]

    if 'rsi' not in show_advanced:
        r_price = 1
        r_volume = 2
        r_macd = 3
        w_macd = 1
        row_heights = [0.5, 0.3, 0.2]

    if ('rsi' not in show_advanced) and ('macd' not in show_advanced):
        r_price = 1
        r_volume = 2
        row_heights = [0.6, 0.4]

    fig = make_subplots(rows=num_indices + 1, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                        # subplot_titles=('Price', 'Volume'),
                        row_heights=row_heights)

    fig.append_trace(
        go.Candlestick(
            x=data.index,
            open=data['open'], high=data['high'],
            low=data['low'], close=data['close'],
            increasing_line_color=colors[0],
            decreasing_line_color=colors[1]
        ),
        row=r_price, col=1
    )

    # Compute MACD:
    if 'macd' in show_advanced:
        # refers to: https://www.alpharithms.com/calculate-macd-python-272222/
        # Get the 26-day EMA of the closing price
        k = data['close'].ewm(span=12, adjust=False, min_periods=12).mean()
        # Get the 12-day EMA of the closing price
        d = data['close'].ewm(span=26, adjust=False, min_periods=26).mean()
        # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
        macd = k - d
        # Get the 9-Day EMA of the MACD for the Trigger line
        macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
        # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
        macd_h = macd - macd_s
        # Add all of our new values for the MACD to the dataframe
        data['macd'] = data.index.map(macd)
        data['macd_h'] = data.index.map(macd_h)
        data['macd_s'] = data.index.map(macd_s)
        # Fast Signal (%k)
        fig.append_trace(
            go.Scatter(
                x=data.index,
                y=data['macd'],
                line=dict(color='#ff9900', width=w_macd),
                name='macd',
                showlegend=True,
                legendgroup='2',
            ), row=r_macd, col=1
        )
        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=data.index,
                y=data['macd_s'],
                line=dict(color='#000000', width=w_macd),
                showlegend=True,
                legendgroup='2',
                name='signal'
            ), row=r_macd, col=1
        )
        # Colorize the histogram values
        colors = np.where(data['macd_h'] < 0, '#000', '#ff9900')
        # Plot the histogram
        fig.append_trace(
            go.Bar(
                x=data.index,
                y=data['macd_h'],
                name='histogram',
                marker_color=colors,
            ), row=r_macd, col=1
        )

    # Compute RSI:
    if 'rsi' in show_advanced:
        delta = data['close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False).mean()
        ema_down = down.ewm(com=13, adjust=False).mean()
        rs = ema_up/ema_down
        data['RSI'] = 100 - (100/(1+rs))

        fig.append_trace(
            go.Scatter(
                x=data.index, 
                y=data['RSI'], 
                name='RSI', 
                line=dict(width=w_rsi)
              ),
            row=r_rsi,
            col=1
        )

        fig.add_hline(y=70, line_dash="dot", row=r_rsi, col="all",
                  annotation_text="70%", 
                  annotation_position="bottom right")

        fig.add_hline(y=30, line_dash="dot", row=r_rsi, col="all",
                  annotation_text="30%", 
                  annotation_position="bottom right")

    # show volume    
    if 'volume' in show_advanced:
        fig.append_trace(
            go.Bar(
                x=data.index,
                y=data['volume'],
                name='Volume'
            ),
        row=r_volume, col=1)

    fig.update_layout(
        title=title,
        yaxis_title='Price',
        xaxis_title='Date',
        width=width,
        height=height,
        showlegend=True
    )

    fig.show()

def vnquant_candle_stick(data,
                          title=None,
                          xlab='Date', ylab='Price',
                          start_date=None, end_date=None,
                          colors=['blue', 'red'],
                          width=800, height=600,
                          data_source='VND',
                          show_advanced=['volume', 'macd', 'rsi'],
                          **kargs):
    '''
    This function is to visualize a candle stick stock index with advanced metrics
    Args:
        data (string or pandas DataFrame): stock data
        title (string: None): title of figure plot
        xlab (string: 'Date'): x label
        ylab (string: 'Price'): y label
        start_date (string: 'yyyy-mm-dd'): start date
        end_date (string: 'yyyy-mm-dd'): end date
        colors (list: ['blue', 'red']): list colors of up and down candle
        width (int: 800): width of graph figure
        height (int: 600): height of graph figure
        data_source (string: 'VND'): data source to get stock price belonging to ['VND', 'CAFE']
        show_advanced (list: ['volume', 'macd', 'rsi']): list of advanced stock index to show up. Each element belongs to ['volume', 'macd', 'rsi'] 
        
    Example:
        from vnquant import plot as pl
        pl.vnquant_candle_stick(
            data='TCB',
            title='TCB symbol from 2022-01-01 to 2022-10-01',
            xlab='Date', ylab='Price',
            start_date='2022-01-01',
            end_date='2022-10-01',
            data_source='CAFE',
            show_advanced = ['volume', 'macd', 'rsi']
        )
    '''
    # Download data from source
    if isinstance(data, str):
        vnquant_candle_stick_source(symbol=data, start_date=start_date, end_date=end_date,
                                     colors=colors, width=width,
                                     height=height, show_advanced=show_advanced,
                                     data_source=data_source)
    else:
        if 'volume' in show_advanced:
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

        if 'volume' in show_advanced:
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
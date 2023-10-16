# ---------------------------------------------------------------------------
# project: vn_quant_upgrade
# author: binh.truong
# date: 1st Jan 2023
# ---------------------------------------------------------------------------
#TODO: Add color different for each WMA


import pandas as pd
import numpy as np
from typing import List, Union
from datetime import datetime, timedelta
from vnquant.data import VND_OHLCV
from vnquant.utils.utils import date_difference_description, date_string_to_timestamp_utc7, datetime_to_timestamp_utc7
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _plot_daily_data(
    data: pd.DataFrame = None, 
    title: str = None,
    WMA: Union[int, List[int]] = None,
    show_vol: bool = False,
    symbol: str = None,
    start_date: Union[str, datetime] = None, 
    end_date: Union[str, datetime] = None,
    **kwargs
) -> None:
    """
    Plot daily data for time periods less than a month,
    When the function plot_data is called, it will classify the time periods to decide the resolution 
        -> daily or yearly type of plot.
        -> This function will display the daily plot.
    The plot type will be candle stick chart.
    ------------
    Args:
        data: (pd.DataFrame) -> A DataFrame containing stock data.
        title: (str) -> Title of the plot (user can customize theri own title, otherwise it will be default)
        WMA: (int or list) -> List of WMA (Ex. [10, 20, 30]), 
            User can input only one WMA (Ex. 10) or a list of WMA (Ex. [10, 20, 30])
        show_vol: (bool) -> True if user want to show the volume of the stock, otherwise False
        symbol: (str) -> Stock symbol (Ex. VNM, VCB, ...)
        start_date: (str) -> Start date of the plot, with format: YYYY-MM-DD
        end_date: (str) -> End date of the plot, with format: YYYY-MM-DD
    Returns:
        Interactive plotly chart: .html file
    """
    row_heights = [1.0]     # default row height
    num_indices = 0         # default number of indices
    if show_vol:
        num_indices = 1
        row_heights = [0.8, 0.2]

    if WMA:
        raise Exception('Time period is too short to display weekly moving average.')
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=num_indices+1, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02, 
        row_heights=row_heights
    )

    # Add the candlestick chart to the top subplot
    fig.add_trace(
        go.Candlestick(
            x=data['Date'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            hovertext=[
                f"Open: {open_}<br>Close: {close}<br>High: {high}<br>Low: {low}<br>Volume: {volume}"
                for open_, close, high, low, volume in zip(
                    data['open'], 
                    data['close'], 
                    data['high'], 
                    data['low'], 
                    data['volume']
                )
            ],
            hoverinfo="y",
        ), 
        row=1, col=1
    )

    # show volume if the user want to (default show_vol value is False)
    if show_vol:
        data['PriceChange'] = data['close'] - data['open']
        data['VolumeColor'] = '#00A86B'     # Default color is 00A86B
        data.loc[data['PriceChange'] < 0, 'VolumeColor'] = '#FF2400'
        fig.append_trace(
            go.Bar(
                x=data['Date'],
                y=data['volume'],
                name='Volume',
                yaxis='y2',     # Use a second y-axis for volume
                marker=dict(color=data['VolumeColor'])
            ),
            row=2, col=1
        )

    # Update the layout to allow zooming by day, month, and hour
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1H", step="hour", stepmode="backward"),
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor='lightgrey',    # Set the background color of the button area
            activecolor='blue'      # Set the color of the active button
        ),
        rangebreaks=[
            dict(bounds=["sat", "mon"]),                   # hide weekends, eg. hide sat to before mon
            dict(bounds=[14.30, 9.25], pattern="hour"),    # hide hours outside of 9.30am-3pm
            dict(bounds=[11.30, 13], pattern="hour"),      # hide hours outside of 9.30am-4pm
        ]
    )

    fig.update_yaxes(type="log")
    fig.update_layout(
        xaxis_rangeslider_visible=False, 
        template='plotly_dark',
        xaxis_title='Date', 
        yaxis_title='Price', 
        title=title if title else '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date),
        hovermode='x unified',
    )

    fig.show()


def _plot_yearly_data(
    data: pd.DataFrame, 
    title: str = None,
    WMA: Union[int, List[int]] = None,
    show_advanced: List[str] = None,
    symbol: str = None,
    start_date: Union[str, datetime] = None, 
    end_date: Union[str, datetime] = None,
    **kwargs
) -> None:
    """
    Plot daily data for time periods less than a month,
    When the function plot_data is called, it will classify the time periods to decide the resolution 
        -> daily or yearly type of plot.
        -> This function will display the yearly plot.
    The plot type will be candle stick chart.
    ------------
    Args:
        data: (pd.DataFrame) -> A DataFrame containing stock data.
        title: (str) -> Title of the plot (user can customize theri own title, otherwise it will be default)
        WMA: (int or list) -> List of WMA (Ex. [10, 20, 30]), 
            User can input only one WMA (Ex. 10) or a list of WMA (Ex. [10, 20, 30])
        show_advanced: (list) -> List of advanced plot (Ex. ['macd', 'rsi', 'volume'])
            User can input only one advanced plot (Ex. ['macd']) or a list of advanced plot (Ex. ['macd', 'rsi', 'volume'])
        symbol: (str) -> Stock symbol (Ex. VNM, VCB, ...)
        start_date: (str) -> Start date of the plot, with format: YYYY-MM-DD
        end_date: (str) -> End date of the plot, with format: YYYY-MM-DD
    Returns:
        Interactive plotly chart: .html file
    """
    row_heights = [1.0]     # default row height
    num_indices = 0         # default number of indices
    r_price = 1             # default row of price

    if show_advanced:
        num_indices = len(show_advanced)

        if num_indices == 3:
            r_price = 1
            r_volume = 2
            r_macd = 3
            r_rsi = 4
            w_macd = 1
            w_rsi = 1
            row_heights = [0.4, 0.2, 0.15, 0.15]

        if 'macd' not in show_advanced:
            r_price = 1
            r_volume = 2
            r_rsi = 3
            w_rsi = 1
            row_heights = [0.6, 0.2, 0.2]

        if 'rsi' not in show_advanced:
            r_price = 1
            r_volume = 2
            r_macd = 3
            w_macd = 1
            row_heights = [0.6, 0.2, 0.2]

        if ('rsi' not in show_advanced) and ('macd' not in show_advanced):
            r_price = 1
            r_volume = 2
            row_heights = [0.7, 0.3]

    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=num_indices+1, 
        cols=1, shared_xaxes=True, 
        vertical_spacing=0.02, 
        row_heights=row_heights
    )

    # Add the candlestick chart to the top subplot
    fig.add_trace(
        go.Candlestick(
            x=data['Date'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            hovertext=[
                f"Open: {open_}<br>Close: {close}<br>High: {high}<br>Low: {low}<br>Volume: {volume}"
                for open_, close, high, low, volume in zip(
                    data['open'], 
                    data['close'], 
                    data['high'], 
                    data['low'], 
                    data['volume']
                )
            ],
            hoverinfo="y",
        ), 
        row=r_price, col=1
    )

    if WMA: # if WMA is int, convert it to list
        if isinstance(WMA, int):
            WMA = [WMA]
        for wma in WMA:
            data[f'{wma}wma'] = data['close'].rolling(window=wma).mean()
            fig.add_trace(
                go.Scatter(
                    x=data['Date'],
                    y=data[f'{wma}wma'],
                    name=f'{wma} week ma',
                    line=dict(color='grey', width=2, dash='dash')
                )
            )
    """
    Logic to compute MACD, RSI if the user want to show advanced plot
    The plot will be displayed in the following order:
        - Price (Candle stick chart -> default)
        - Volume (Bar chart -> if the user want to show volume)
        - MACD (Line chart -> if the user want to show MACD)
        - RSI (Line chart -> if the user want to show RSI)
    """
    # Compute MACD:
    if show_advanced and 'macd' in show_advanced:
        # refers to: https://www.alpharithms.com/calculate-macd-python-272222/
        k = data['close'].ewm(span=12, adjust=False, min_periods=12).mean()     # Get the 26-day EMA of the closing price
        d = data['close'].ewm(span=26, adjust=False, min_periods=26).mean()     # Get the 12-day EMA of the closing price
        macd = k - d                                                            # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
        macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()           # Get the 9-Day EMA of the MACD for the Trigger line
        macd_h = macd - macd_s                                                  # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
        data['macd'] = data.index.map(macd)                                     # Add all of our new values for the MACD to the dataframe
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
                line=dict(color='#012345', width=w_macd),
                showlegend=True,
                legendgroup='2',
                name='signal'
            ), row=r_macd, col=1
        )
        # Colorize the histogram values
        colors = np.where(data['macd_h'] < 0, '#000', '#ff9900')
        fig.append_trace(
            go.Bar(
                x=data.index,
                y=data['macd_h'],
                name='histogram',
                marker_color=colors,
            ), row=r_macd, col=1
        )

    # Compute RSI:
    if show_advanced and 'rsi' in show_advanced:
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
            row=r_rsi, col=1
        )

        fig.add_hline(y=70, line_dash="dot", row=r_rsi, col="all",
                annotation_text="70%", 
                annotation_position="bottom right")

        fig.add_hline(y=30, line_dash="dot", row=r_rsi, col="all",
                annotation_text="30%", 
                annotation_position="bottom right")

    # show volume    
    if show_advanced and 'volume' in show_advanced:
        # Calculate price changes
        data['PriceChange'] = data['close'] - data['open']
        data['VolumeColor'] = '#00A86B'     # Default color is 00A86B
        data.loc[data['PriceChange'] < 0, 'VolumeColor'] = '#FF2400'
        # Add volume bars to the figure
        fig.append_trace(
            go.Bar(
                x=data['Date'],
                y=data['volume'],
                name='Volume',
                yaxis='y2',     # Use a second y-axis for volume
                marker=dict(color=data['VolumeColor'])
            ),
            row=r_volume, col=1
        )

    # Update the layout to allow zooming by day, month, and hour
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor='lightgrey',     # Set the background color of the button area
            activecolor='blue'       # Set the color of the active button
        ),
        rangebreaks=[
            dict(bounds=["sat", "mon"]),     # hide weekends, eg. hide sat to before mon
        ]
    )

    fig.update_yaxes(type="log")
    fig.update_layout(
        xaxis_rangeslider_visible=False, 
        template='plotly_dark',
        xaxis_title='Date', 
        yaxis_title='Price', 
        title= title if title else '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date),
        hovermode='x unified',
    )
    
    fig.show()


def plot_data(
    data: Union[str, pd.DataFrame],
    title: str = None,
    WMA: int = None,
    show_advanced: List[str] = None,
    start_date: Union[str, datetime] = None, 
    end_date: Union[str, datetime] = None,
    **kwargs
) -> None:
    """
    Plot a specific stock data from user input.
    The data argument can be a stock symbol (Ex. VNM, VCB, ...) or a DataFrame containing stock data.
    If the data is a specific stock symbol, the dataframe will be requested from VNDIRECT API (using VND_OHLCV class)
    If the data is a dataframe, it must contain these columns: ['Date', 'open', 'high', 'low', 'close'], 'volume' is optional
    If data is dataframe and user want to display volume, the dataframe must contain 'volume' column.
    User will call this function to plot the stock data.
    If the time period is less than a month, the plot type will be daily candle stick chart.
    If the time period is more than a month, the plot type will be yearly candle stick chart.
    ------------
    Args:
        data: (str or pd.DataFrame) -> A DataFrame containing stock data.
        title: (str) -> Title of the plot
        WMA: (int or list) -> List of WMA (Ex. [10, 20, 30]),
                            User can input only one WMA (Ex. 10) or a list of WMA (Ex. [10, 20, 30])
        show_advanced: (list) -> List of advanced plot (Ex. ['macd', 'rsi', 'volume'])
        start_date: (str) -> Start date of the plot
        end_date: (str) -> End date of the plot
    Returns:
        Interactive plotly chart: .html file
    """
    if isinstance(data, str):
        symbol = data
        data_loader = VND_OHLCV()     
        time_mark = date_difference_description(end_date, start_date) # Classify time periods to decide the resolution -> daily or yearly type of plot
        start_date_ = int(date_string_to_timestamp_utc7(start_date)) if isinstance(start_date, str) else datetime_to_timestamp_utc7(start_date) # convert start_date to timestamp
        end_date_ = int(date_string_to_timestamp_utc7(end_date)) if isinstance(end_date, str) else datetime_to_timestamp_utc7(end_date)         #convert end_date to timestamp

        if time_mark == 'hours' or time_mark == 'days':
            data_params = {
                'symbol': symbol,
                'resolution': '1',
                'from': start_date_,
                'to': end_date_
            }
            data = data_loader.get_data(data_params) 
            show_vol = False
            if show_advanced:
                show_vol = True
                if 'volume' not in show_advanced:
                    raise Exception('Due to the short time period, this plot can only show volume.')

            _plot_daily_data(
                data=data, 
                title=title, 
                WMA=WMA,
                show_vol=show_vol,
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date
            )

        else:
            data_params = {
                'symbol': symbol,
                'resolution': 'D',
                'from': start_date_,
                'to': end_date_
            }
            data = data_loader.get_data(data_params)     # get data from VNDIRECT API
            _plot_yearly_data(
                data=data, 
                title=title, 
                WMA=WMA,
                show_advanced=show_advanced,
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date
            )
    else:
        index = data['Date']
        if not isinstance(index, pd.core.indexes.datetimes.DatetimeIndex):
            raise IndexError('Index of dataframe must be DatetimeIndex!')
        if not start_date:
            start_date = min(index)
        if not end_date:
            end_date = max(index)

        time_mark = date_difference_description(end_date, start_date)
        if time_mark == 'hours' or 'days':
            show_vol = False
            if show_advanced:
                show_vol = True
                if 'volume' not in show_advanced:
                    raise Exception('Due to the short time period, this plot can only show volume.')
                if 'volume' not in data.columns:
                    raise Exception('The input dataframe must contains volume feature.')

            _plot_daily_data(
                data=data, 
                title=title, 
                WMA=WMA,
                show_vol=show_vol,
                start_date=start_date, 
                end_date=end_date
            )
        
        else:
            _plot_yearly_data(
                data=data, 
                title=title, 
                WMA=WMA,
                show_advanced=show_advanced,
                start_date=start_date, 
                end_date=end_date
            )


if __name__ =="__main__":
    # plot_data(data='VNM', start_date='2021-08-11', end_date='2021-10-13')
    # plot_data(data='VNM', start_date=datetime.now() - timedelta(days=5), end_date=datetime.now())
    # plot_data(data='VNM', show_advanced=['volume'], start_date=datetime.now() - timedelta(days=30), end_date=datetime.now())
    # plot_data(data='VNM', WMA=[5, 10], show_advanced=['volume'], start_date=datetime.now() - timedelta(days=365), end_date=datetime.now())
    # plot_data(data='VNM', WMA=[5, 10], show_advanced=['volume', 'macd'], start_date='2023-08-01', end_date='2023-10-13')
    # plot_data(data='VNM', title='test plot', WMA=[5, 10], show_advanced=['volume', 'macd'], start_date='2023-04-01', end_date='2023-10-13')    
    plot_data(data='VNM', show_advanced=['volume'], start_date='2023-10-11', end_date='2023-10-13')



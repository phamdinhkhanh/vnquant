# ---------------------------------------------------------------------------
# project: vn_quant_update
# author: binh.truong
# date: 1st Jan 2023
# ---------------------------------------------------------------------------
#TODO: 1. Add plot for dataframe also (rase exception if the input is dataframe)
#TODO: 2. Add color different for each WMA
#TODO: 3. Add show advanced plot (with MACD, RSI, Bollinger band, ...)

import pandas as pd
from vnquant.data import VND_OHLCV
from vnquant.utils.utils import date_difference_description, date_string_to_timestamp_utc7
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Union


def plot_daily_data(
        data: pd.DataFrame = None, 
        title: str = None,
        WMA: Union[int, List[int]] = None,
        show_vol: bool = False,
        symbol: str = None,
        start_date: str = None, 
        end_date: str = None,
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
    if WMA:
        raise Exception('Time period is too short to display weekly moving average.')
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.8, 0.2])

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
        # Add volume bars to the figure
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['volume'],
            name="Volume",
            yaxis='y2',  # Use a second y-axis for volume
            marker=dict(color='orange')
        ), row=2, col=1)

    # Update the layout to allow zooming by day, month, and hour
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1H", step="hour", stepmode="backward"),
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor='lightgrey',  # Set the background color of the button area
            activecolor='blue'  # Set the color of the active button
        ),
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[14.30, 9.25], pattern="hour"),  # hide hours outside of 9.30am-3pm
            dict(bounds=[11.30, 13], pattern="hour"),  # hide hours outside of 9.30am-4pm
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


def plot_yearly_data(
        data: pd.DataFrame, 
        title: str = None,
        WMA: Union[int, List[int]] = None,
        show_vol: bool = False,
        symbol: str = None,
        start_date: str = None,
        end_date: str = None,
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
        show_vol: (bool) -> True if user want to show the volume of the stock, otherwise False
        symbol: (str) -> Stock symbol (Ex. VNM, VCB, ...)
        start_date: (str) -> Start date of the plot, with format: YYYY-MM-DD
        end_date: (str) -> End date of the plot, with format: YYYY-MM-DD
    Returns:
        Interactive plotly chart: .html file
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.8, 0.2])

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

    if isinstance(WMA, int): # if WMA is int, convert it to list
        WMA = [WMA]
    # Add WMA to the plot
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
    
    # show volume if the user want to (default show_vol value is False)
    if show_vol:
        # Add volume bars to the figure
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['volume'],
            name="Volume",
            yaxis='y2',  # Use a second y-axis for volume
            marker=dict(color='orange')
        ), row=2, col=1)

    # Update the layout to allow zooming by day, month, and hour
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor='lightgrey',  # Set the background color of the button area
            activecolor='blue'  # Set the color of the active button
        ),
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
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
    show_vol: bool = False,
    start_date: str = None, 
    end_date: str = None,
) -> None:
    """
    Plot a specific stock data from user input.
    The data will be requested from VNDIRECT API (using VND_OHLCV class)
    User will call this function to plot the stock data.
    If the time period is less than a month, the plot type will be daily candle stick chart.
    If the time period is more than a month, the plot type will be yearly candle stick chart.
    ------------
    Args:
        data: (str or pd.DataFrame) -> A DataFrame containing stock data.
        title: (str) -> Title of the plot
        WMA: (int or list) -> List of WMA (Ex. [10, 20, 30]),
                            User can input only one WMA (Ex. 10) or a list of WMA (Ex. [10, 20, 30])
        show_vol: (bool) -> True if user want to show the volume of the stock, otherwise False
        start_date: (str) -> Start date of the plot
        end_date: (str) -> End date of the plot
    Returns:
        Interactive plotly chart: .html file
    """
    if isinstance(data, str):
        symbol = data
        data_loader = VND_OHLCV()

        # Classify time periods to decide the resolution -> daily or yearly type of plot
        time_mark = date_difference_description(end_date, start_date)
        if time_mark == 'hours' or time_mark == 'days':
            data_params = {
                'symbol': symbol,
                'resolution': '1',
                'from': int(date_string_to_timestamp_utc7(start_date)),
                'to': int(date_string_to_timestamp_utc7(end_date)),
            }
            data = data_loader.get_data(data_params) # get data from VNDIRECT API
            plot_daily_data(
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
                'from': int(date_string_to_timestamp_utc7(start_date)),
                'to': int(date_string_to_timestamp_utc7(end_date)),
            }
            data = data_loader.get_data(data_params) # get data from VNDIRECT API
            plot_yearly_data(
                data=data, 
                title=title, 
                WMA=WMA,
                show_vol=show_vol,
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date
            )


if __name__ =="__main__":
    plot_data(data='VNM', WMA=[10, 20, 30], show_vol=True, start_date='2023-03-01', end_date='2023-10-07')



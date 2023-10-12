# ---------------------------------------------------------------------------
# project: vn_quant_update
# author: binh.truong
# date: 1st Jan 2023
# ---------------------------------------------------------------------------

import pandas as pd
from vnquant.data import VND_OHLCV
from vnquant.utils.utils import date_difference_description, date_string_to_timestamp_utc7
import plotly.graph_objects as go


def plot_daily_data(
        data: pd.DataFrame = None, 
        title: str = None,
        symbol: str = None,
        start_date: str = None, 
        end_date: str = None,
    ) -> None:
    """
    Plot daily data for time periods less than a month
    ------------
    Args:
        data: (pd.DataFrame) -> A DataFrame containing stock data.
    Returns:
        Interactive plotly chart: .html file
    """
    fig = go.Figure(
        data=[
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
            )
        ]
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
        symbol: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> None:
    """
    Plot yearly data for time periods more than a month
    ------------
    Args:
        data: (pd.DataFrame) -> A DataFrame containing stock data.
    Returns:
        Interactive plotly chart: .html file
    """
    data['20wma'] = data['close'].rolling(window=20).mean()
    fig = go.Figure(
        data=[
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
            )
        ]
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['20wma'],
            name='20 week ma',
            line=dict(color='grey', width=2, dash='dash')
        )
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
    data: str | pd.DataFrame,
    title: str = None,
    start_date: str = None, 
    end_date: str = None,
) -> None:
    """
    Plot stock data from VNDIRECT API
    ------------
    Args:
        data: (str or pd.DataFrame) -> A DataFrame containing stock data.
        title: (str) -> Title of the plot
        start_date: (str) -> Start date of the plot
        end_date: (str) -> End date of the plot
    Returns:
        Interactive plotly chart: .html file
    """
    if isinstance(data, str):
        symbol = data
        data_loader = VND_OHLCV()
        time_mark = date_difference_description(end_date, start_date)
        # Classify time periods to decide the resolution -> daily or yearly type of plot
        if time_mark == 'hours' or time_mark == 'days':
            data_params = {
                'symbol': symbol,
                'resolution': '1',
                'to': int(date_string_to_timestamp_utc7(start_date)),
                'from': int(date_string_to_timestamp_utc7(end_date)),
            }
            data = data_loader.get_data(data_params) # get data from VNDIRECT API
            plot_daily_data(
                data=data, 
                title=title, 
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date
            )
        else:
            data_params = {
                'symbol': symbol,
                'resolution': 'D',
                'to': int(date_string_to_timestamp_utc7(start_date)),
                'from': int(date_string_to_timestamp_utc7(end_date)),
            }
            data = data_loader.get_data(data_params) # get data from VNDIRECT API
            plot_yearly_data(
                data=data, 
                title=title, 
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date
            )


if __name__ =="__main__":
    plot_data(data='VMN', start_date='2021-09-01', end_date='2021-11-01')



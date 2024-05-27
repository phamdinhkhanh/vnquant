# 1. Test data loader
import vnquant.data as dt
# loader = dt.DataLoader('E1VFVN30', '2021-02-01','2021-04-02', data_source='VND', minimal=True)
# data = loader.download()
# print(data)

# loader = dt.DataLoader('E1VFVN30', '2021-02-01','2021-04-02', data_source='CAFE', minimal=True)
# data = loader.download()
# print(data)

# loader = dt.DataLoader(['VCB', 'TCB'], '2021-02-01','2021-04-02', data_source='CAFE', minimal=True, table_style='prefix')
# data = loader.download()
# print(data)

# 2. Test clone finance
# import vnquant.data as dt
# loader = dt.FinanceLoader('VND', '2019-06-02','2021-12-31', data_source='VND', minimal=True)
# data_business = loader.get_business_report()
# print(data_business.head())
# data_business.head().to_html('data_business.html')

# import vnquant.data as dt
# loader = dt.FinanceLoader('VND', '2019-06-02','2021-12-31', data_source='VND', minimal=True)
# data_finan = loader.get_finan_report()
# print(data_finan.head())
# data_finan.head().to_html('data_finan.html')


# import vnquant.data as dt
# loader = dt.FinanceLoader('VND', '2019-06-02','2021-12-31', data_source='VND', minimal=True)
# data_cash = loader.get_cashflow_report()
# print(data_cash.head())
# data_cash.head().to_html('data_cashflow.html')

# import vnquant.data as dt
# loader = dt.FinanceLoader('VND', '2019-06-02','2020-12-31', data_source='VND', minimal=True)
# data_basic = loader.get_basic_index()
# print(data_basic.head())
# data_basic.head().to_html('data_basic.html')

# import vnquant.plot as pl
# pl.vnquant_candle_stick_source(
#     symbol='VCB',
#     start_date='2019-06-02', end_date='2024-05-27',
#     colors=['blue', 'red'],
#     width=1600, height=1200,
#     show_advanced=['volume', 'macd', 'rsi'],
#     data_source='cafe', # not support vnd
# )

# from vnquant import plot as pl
# pl.vnquant_candle_stick(
#     data='VND',
#     title='VND symbol from 2019-09-01 to 2019-11-01',
#     xlab='Date', ylab='Price',
#     start_date='2019-09-01',
#     end_date='2019-11-01',
#     data_source='CAFE',
#     show_advanced=['volume', 'macd', 'rsi']
# )

# symbol,
#         start_date, end_date,
#         colors=['blue', 'red'],
#         width=800, height=600,
#         data_source='VND',
#         show_advanced = ['volume', 'macd', 'rsi'],

# import vnquant.plot as pl2
# import pandas as pd
# from datetime import datetime, timedelta

# # plot data based on stock symbol
# pl2.plot_data(data='VNM', start_date='2021-08-11', end_date='2021-10-13')
# pl2.plot_data(data='VNM', start_date=datetime.now()-timedelta(days=5), end_date=datetime.now())
# pl2.plot_data(data='VNM', show_advanced=['volume'], start_date=datetime.now()-timedelta(days=1), end_date=datetime.now())
# pl2.plot_data(data='VNM', WMA=[5, 10], show_advanced=['volume'], start_date=datetime.now() - timedelta(days=365), end_date=datetime.now())
# pl2.plot_data(data='VNM', WMA=[5, 10], show_advanced=['volume', 'macd'], start_date='2023-08-01', end_date='2023-10-13')
# pl2.plot_data(data='VNM', title='test plot', WMA=[5, 10], show_advanced=['volume', 'macd'], start_date='2023-04-01', end_date='2023-10-13')    
# pl2.plot_data(data='VNM', show_advanced=['volume'], start_date='2023-10-11', end_date='2023-10-13')

# # # plot data based on dataframe
# df = pd.read_csv(r'C:\Users\binh.truong\Code\vnquant\data.csv')
# pl2.plot_data(data=df, show_advanced=['volume', 'macd', 'rsi'])

# # plot data based on directory
# pl2.plot_data(r'C:\Users\binh.truong\Code\vnquant\data.csv')



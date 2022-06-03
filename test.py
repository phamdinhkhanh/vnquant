# # 1. Test data loader
# import vnquant.data as dt
# loader = dt.DataLoader('E1VFVN30', '2021-02-01','2021-04-02', data_source='VND', minimal=True)
# data = loader.download()
# print(data)

# # 2. Test clone finance
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
# pl._vnquant_candle_stick_source('VND', '2019-09-01', '2019-11-01', show_vol=False)

# from vnquant import utils
# print(utils._isOHLC)
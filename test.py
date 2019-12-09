# Test data loader
import vnquant.DataLoader as dl
loader = dl.DataLoader('VND', '2018-02-02','2018-04-02')
loader.download()

# Test visualizatioin
from vnquant import plot
plot._vnquant_candle_stick(data='VND',
                           title='VND stock price data and volume',
                           xlab='Date', ylab='Price',
                           start_date='2019-09-01', end_date='2019-11-01',
                           show_vol=True)
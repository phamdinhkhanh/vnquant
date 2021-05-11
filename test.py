# Test data loader
import vnquant.DataLoader as dl
loader = dl.DataLoader('VND', '2018-02-02','2018-04-02', data_source='VND', minimal=True)
data = loader.download()
print(data.head())
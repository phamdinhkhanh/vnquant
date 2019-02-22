# VNDS package

## Introduction

This project provide the financial information and useful visualization instrument about Vietnam stock market to researcher.
Particularly, there are many aspect of data relating to any stock being able to store and clone. The official version are
built on both machine learning language Python and R.

## Clone Stock Prices:

You can load the prices of one or more stocks in specific time interval according to syntax as below.
```{python}
DataLoader(symbols='VND',
           start="2018-01-10",
           end="2018-02-15",
           minimal=True,
           data_source='vnd')
```
**Arguments**

* `symbols`: a string or list of strings indicate the stock names.
* `start`: start date time with format `yyyy-mm-dd`.
* `end`: end date time with format `yyyy-mm-dd`.
* `minimal`: default is True, we only clone `high, low, open, close, adjust price, volume` of stocks. In contrast, more information is added,
for example `volumn_reconcile, volumn_match,...`
* `data_source`: the source to clone the stock prices. Currently, there two main resources are `Vndirect` and `Cafef`.

### Clone one stock:
```{python}
from VNDS import DataLoader
loader = DataLoader(symbols='VND', start="2018-01-10", end="2018-02-15", minimal=True, data_source='vnd')
data = loader.download()
data.head()
```
### Clone more stocks:
```{python}
loader = DataLoader(symbols=['VND', 'VCB'], start="2018-01-10", end="2018-02-15", minimal=True, data_source='vnd')
data = loader.download()
data.head()
```

| Dataset                | Classes | Train samples | Test samples |
|------------------------|:---------:|:---------------:|:--------------:|
| AG’s News              |    4    |    120 000    |     7 600    |
| Sogou News             |    5    |    450 000    |    60 000    |
| DBPedia                |    14   |    560 000    |    70 000    |
| Yelp Review Polarity   |    2    |    560 000    |    38 000    |
| Yelp Review Full       |    5    |    650 000    |    50 000    |
| Yahoo! Answers         |    10   |   1 400 000   |    60 000    |
| Amazon Review Full     |    5    |   3 000 000   |    650 000   |
| Amazon Review Polarity |    2    |   3 600 000   |    400 000   |

## Setting:
This project is in developing process, So It is distributed only in github. Installing it as following:
```
clone https....
cd VNDS
python install setting
```


<img src="visualization/ag_news_small.png" width="420"> <img src="visualization/ag_news_large.png" width="420">

- **sogou_news**

<img src="visualization/sogou_news_small.png" width="420"> <img src="visualization/sogou_news_large.png" width="420">

- **db_pedia**

<img src="visualization/dbpedia_small.png" width="420"> <img src="visualization/dbpedia_large.png" width="420">

- **yelp_polarity**

<img src="visualization/yelp_review_polarity_small.png" width="420"> <img src="visualization/yelp_review_polarity_large.png" width="420">

- **yelp_review**

<img src="visualization/yelp_review_full_small.png" width="420"> <img src="visualization/yelp_review_full_large.png" width="420">

- **amazon_review**

<img src="visualization/amazon_review_full_small.png" width="420"> <img src="visualization/amazon_review_full_large.png" width="420">

- **amazon_polarity**

<img src="visualization/amazon_review_polarity_small.png" width="420"> <img src="visualization/amazon_review_polarity_large.png" width="420">

Through this project, i hope you make your work being more covinient and easy by applying them. Though try hard, but there are many drawback,
kindly comment and send me feed back to implement my project.

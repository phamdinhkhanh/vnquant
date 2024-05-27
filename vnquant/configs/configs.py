# Copyright (c) vnquant. All rights reserved.
# Can be used to randomize and rotate

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
]

STOCKS_DATA = {}

FINANCE_DATA = {}

# Config for DataLoader
URL_VND = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
URL_CAFE = "https://s.cafef.vn/Ajax/PageNew/DataHistory/PriceHistory.ashx"
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}

STOCK_COLUMNS=[
    'code', 'date', 'floor', 
    'basic_price', 'ceiling_price', 'floor_price',
    'close', 'open', 'high', 'low', 'average',
    'adjust_close', 'adjust_open', 'adjust_high', 'adjust_low', 'adjust_average',
    'change', 'adjust_change', 'percent_change',
    'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile'
]

STOCK_COLUMNS_CAFEF=[
    'code', 'date',
    'close', 'open', 'high', 'low', 'adjust_price', 'change_str',
    'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile'
]

STOCK_COLUMNS_CAFEF_FINAL=[
    'code', 'date',
    'close', 'open', 'high', 'low', 'adjust_price', 'change', 'percent_change',
    'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile'
]

REGEX_PATTERN_PRICE_CHANGE_CAFE = r'([-+]?\d*\.\d+|\d+)\s*\(\s*([-+]?\d*\.\d+|\d+)\s*%\s*\)'

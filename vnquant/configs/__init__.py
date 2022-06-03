# Copyright (c) general_backbone. All rights reserved.
# from .configs import USER_AGENTS, URL_VND, URL_CAFE, HEADERS

# Copyright (c) general_backbone. All rights reserved.
# Can be used to randomize and rotate
# Source(s):
# - https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
]

# Config for DataLoader
URL_VND = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
URL_CAFE = "http://s.cafef.vn/Lich-su-giao-dich-"
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}

__all__ = [
    'USER_AGENTS', 'URL_VND', 'URL_CAFE', 'HEADERS'
]
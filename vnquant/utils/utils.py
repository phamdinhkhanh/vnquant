# Copyright (c) general_backbone. All rights reserved.
from datetime import datetime
import re
import random
import requests
import logging
import urllib.parse
from copy import deepcopy
from typing import List
from vnquant.configs import USER_AGENTS

def clean_text(text):
    return re.sub('[(\n\t)*]', '', text).strip()

def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

def split_change_col(text):
    return re.sub(r'[\(|\)%]', '', text).strip().split()

def extract_number(text):
    return int(re.search(r'\d+', text).group(0))


def _isOHLC(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False


def _isOHLCV(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open', 'volume']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False


# Based on the industry classification API from VNDirect
# Basic query param structure:
#   :params:
#       q: the core part of the query; possible inputs:
#           - codeList: list of string; tickers to query
#           - industryCode: string; the industry code to query
#           - industryLevel: int or list of int; range from 1 to 3;
#               with 1 being the highest industry level and 3 the lowest
#           - higherLevelCode: string; the industry code of
#               the higher level to query
#           - englishName: part of the English name
#               of the industry to query
#           - vietnameseName: part of the Vietnamese name
#               of the industry to query
#       size: the number of "elements" in a query result page;
#           with an element representing an industry

# TODO: How to deal with a Vietnamese name query?

# Constants
# Susceptible to API change
CONTENT_TYPE = "application/json"
MAX_QUERY_SIZE = 9999
BASE_URL = "https://finfo-api.vndirect.com.vn/v4/industry_classification"
PAYLOAD_Q_KEYS = {
    'codeList': "",
    'industryCode': "",
    'industryLevel': "",
    'higherLevelCode': "",
    'englishName': "",
    'vietnameseName': ""
}
PAYLOAD_Q_JOIN_CHAR = "~"
BASE_PAYLOAD = {
    'q': "",
    'size': ""
}
PAYLOAD_SAFE_CHARS = ":," # Not to encode these in query param

def get_ind_class(
        code_list: List[str]=[],
        industry_codes: List[str]=[],
        industry_levels: List[str]=[],
        higher_level_codes: List[str]=[],
        english_name: str="",
        vietnamese_name: str="",
        result_size: int=MAX_QUERY_SIZE
    ) -> dict:
    '''Gets industries and their available tickers

    :params:
        @code_list: list of str - tickers
        @industry_codes: list of str - industry codes
        @industry_levels: list of str - industry levels
        @higher_level_codes: list of str - higher industry level's codes
        @english_name: str - part of the industry's English name to query for
        @vietnamese_name: str - part of the industry's Vietnamese name to query for
        @result_size: int - the number of industry to include on 1 result page

    :example:
    logging.basicConfig(level=logging.INFO)

    START = '2020-02-02'
    END = '2020-04-02'
    ind_df, meta = get_ind_class(code_list=["ASM", "AAA"])
    p_df = get_price_from_ind_df(ind_df, START, END)

    logging.info(ind_df)
    logging.info(p_df)
    '''
    
    # Prepare payload
    # Construct a single string containing all keys for the 'q' parameter
    payload = deepcopy(BASE_PAYLOAD)
    payload_q_keys = deepcopy(PAYLOAD_Q_KEYS)
    payload_q_keys['codeList'] = ",".join([code for code in code_list])
    payload_q_keys['industryCode'] = ",".join([ic for ic in industry_codes])
    payload_q_keys['industryLevel'] = ",".join([il for il in industry_levels])
    payload_q_keys['higherLevelCode'] = ",".join([hlc for hlc in higher_level_codes])
    payload_q_keys['englishName'] = english_name
    payload_q_keys['englishName'] = vietnamese_name
    payload_q_str = PAYLOAD_Q_JOIN_CHAR.join(
        [f"{key}:{value}" for key, value in payload_q_keys.items()]
    )
    payload['q'] = payload_q_str
    payload['size'] = result_size
    
    payload_str = urllib.parse.urlencode(payload, safe=PAYLOAD_SAFE_CHARS)
    headers = {
        'content-type': CONTENT_TYPE,
        'User-Agent': random.choice(USER_AGENTS)
    }
    
    resp = requests.get(
        BASE_URL,
        params=payload_str,
        headers=headers
    )
 
    print('BASE_URL: ', BASE_URL)
    print('payload_str: ', payload_str)
    print('header: ', headers)
    return resp.json()
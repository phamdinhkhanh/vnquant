from datetime import datetime
import re

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

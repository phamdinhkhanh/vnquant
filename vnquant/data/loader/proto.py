# Copyright (c) vnquant. All rights reserved.
from typing import Union
from vnquant import utils
from vnquant.log.logging import logger

class DataLoadProto():
    def __init__(self, symbols: Union[str, list], start, end, *arg, **karg):
        self.symbols = symbols
        self.start = utils.convert_text_dateformat(start, new_type='%d/%m/%Y')
        self.end = utils.convert_text_dateformat(end, new_type='%d/%m/%Y')

    def pre_process_symbols(self):
        if isinstance(self.symbols, list):
            symbols = self.symbols
            logger.info('Start downloading data symbols: {}, start: {}, end: {}!'.format(symbols, self.start, self.end))
        else:
            symbols = [self.symbols]
            logger.info('Start downloading data symbol: {}, start: {}, end: {}!'.format(self.symbols, self.start, self.end))
        return symbols

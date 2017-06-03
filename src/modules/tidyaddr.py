#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tidyaddr

"""

import sys

import numpy as np
import pandas as pd


class TidyAddr(object):

    def __init__(self, df, column):
        """Wraps a TidyAddr object around a TidyAll dataframe"""

        self.df = df
        self.addr_col = column

    def parse(self):

        print(self.df[self.addr_col])


if __name__ == '__main__':

    df = pd.read_csv("tests/samples/test_addr_csv.csv")
    obj = TidyAddr(df, "PLN Address")
    obj.parse()

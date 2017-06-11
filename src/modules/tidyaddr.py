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

    @staticmethod
    def parse_addr(addr_str):
        """IMPLEMENT TIDYADDR HERE"""

        return ""

    def __clean_col(self):
        """Parses and standardizes the selected column values

        Args:
            None

        Returns:
            None
        """

        if self.addr_col:

            self.df["tidy_addr"] = self.df[self.addr_col].apply(
                lambda x: self.parse_addr(str(x))
            )


if __name__ == '__main__':

    df = pd.read_csv("tests/samples/test_addr_csv.csv")
    obj = TidyAddr(df, "PLN Address")
    obj.parse()

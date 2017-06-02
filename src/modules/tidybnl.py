#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tidybnl

This file declares and implements the TidyBlockNLot classes for TidyAll.
TidyBlockNLot converts integer block and lot columns into string, pads them
with zeros and creates the tidy_blocknlot column.
"""


class TidyBlockNLot(object):

    def __init__(self, df, column):

        self.df = df
        self.block_col = ""
        self.lot_col = ""

        for key, value in column.items():

            if key == "block":
                self.block_col = value

            if key == "lot":
                self.lot_col = value

    @staticmethod
    def parse_col(col_str, pad):

        if any(c.isalpha() for c in col_str):
            return str("0" * pad + col_str)[-pad - 2:]

        return str("0" * pad + col_str)[-pad - 1:]

    def parse(self):

        if self.block_col:

            self.df["tidy_block"] = self.df[self.block_col].astype(str)
            self.df["tidy_block"] = self.df["tidy_block"].apply(
                lambda x: self.parse_col(str(x), 3)
            )

        if self.lot_col:

            self.df["tidy_lot"] = self.df[self.lot_col].astype(str)
            self.df["tidy_lot"] = self.df["tidy_lot"].apply(
                lambda x: self.parse_col(str(x), 2)
            )

        if self.block_col and self.lot_col:

            self.df["tidy_blocknlot"] = self.df[
                "tidy_block"] + " " + self.df["tidy_lot"]

        return self.df

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tidytools

This file declares and implements the TidyDate and TidyBlockNLot classes for
TidyAll.

TidyDate converts and formats valid date columns into ISO 8601 (yyyy-mm-dd).
TidyBlockNLot converts integer block and lot columns into string, pads them
with zeros and creates the tidy_blocknlot column.
"""

from __future__ import absolute_import, print_function, unicode_literals
import sys

from dateutil import parser as date_parser
import numpy as np
import pandas as pd

from .settings import TIDY_DATE_SPLIT


class TidyDate(object):

    def __init__(self, df, column):
        """Wraps a TidyDate object around a TidyAll dataframe"""

        self.df = df
        self.date_col = column

    @staticmethod
    def parse_date(date_str):

        try:
            return date_parser.parse(date_str)

        except (TypeError, ValueError):

            try:

                def split_date():

                    return (date_str[-4:], date_str[:-6], date_str[-6:-4])

                return date_parser.parse('-'.join(split_date()))

            except (TypeError, ValueError):
                return None

    def __clean_col(self):
        """Parses and standardizes the selected column values

        Args:
            None

        Returns:
            None
        """

        if self.date_col:

            if np.dtype(self.df[self.date_col]) == np.dtype("datetime64[ns]"):
                sys.exit("Column is already in date format")

            self.df["tidy_date"] = self.df[self.date_col].apply(
                lambda x: self.parse_date(str(x))
            )

            self.df["tidy_date"] = self.df["tidy_date"].apply(
                lambda x: x.date() if pd.notnull(x) else x
            )

    def __split_date(self):
        """Splits the "tidy_date" column into separate tidy year, month and
        day columns

        Args:
            None

        Returns:
            None
        """

        for index, col in enumerate(TIDY_DATE_SPLIT):

            try:

                self.df[col] = self.df["tidy_date"].apply(
                    lambda x: int(str(x).split("-")[index])
                    if pd.notnull(x) else x
                )

            except IndexError:
                continue

    def __fill_na(self):
        """Fills values that were unable to be parsed with the original values

        Args:
            None

        Returns:
            None
        """

        TIDY_DATE_SPLIT.append("tidy_date")
        for col in TIDY_DATE_SPLIT:
            self.df[col].fillna(self.df[self.date_col], inplace=True)

    def parse(self):

        self.__clean_col()
        self.__split_date()
        self.__fill_na()

        return self.df


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
            return str('0' * pad + col_str)[-pad - 2:]

        return str('0' * pad + col_str)[-pad - 1:]

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
                "tidy_block"] + ' ' + self.df["tidy_lot"]

        return self.df

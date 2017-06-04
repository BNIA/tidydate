#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tidydate

This file declares and implements the TidyDate class for TidyAll.
TidyDate converts and formats valid date columns into ISO 8601 (yyyy-mm-dd).
"""

import sys

from dateutil import parser as date_parser
import numpy as np
import pandas as pd

from settings import TIDY_DATE_SPLIT


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

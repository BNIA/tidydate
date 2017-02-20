#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tidydate

This file implements the date cleaning/tidying of TidyDate. It accepts
*.csv and *.xlsx files and standardizes the specified date column into
ISO 8601 formatted dates (YYYY-MM-DD).
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import remove
import sys
from textwrap import dedent

import dateutil
from numpy import where as np_where
from pandas import notnull, read_csv, read_excel


class TidyDate(object):

    def __init__(self, file_path, debug=False):
        """Constructs a TidyDate object by creating a dataframe from the input
        file

        Args:
            file_path (`str`): path of the uploaded dataset

        Returns:
            None
        """

        self.file_path = file_path
        self.file_name = ""
        self.df = self.to_df()
        self.column = ""
        self.tidy_date_split = [
            "tidy_year",
            "tidy_month",
            "tidy_day"
        ]
        self.debug = debug

    def __del__(self):
        """Destructor to remove the uploaded file after conversion

        Args:
            None

        Returns:
            None
        """

        if not self.debug:
            remove(self.file_path)

    @staticmethod
    def parse_date(date_str):

        try:
            return dateutil.parser.parse(date_str)

        except ValueError:
            return None

    def to_df(self):
        """Converts the input file into a Pandas Dataframe

        Args:
            file_path (`str`): path of the uploaded dataset

        Return:
            file_name (`str`): name of the input file
            (`obj: pandas.Dataframe`): dataframe of the file
        """

        self.file_name, ext = self.file_path.rsplit('.', 1)

        if ext == "csv":
            return read_csv(self.file_path)

        elif ext == "xlsx":
            return read_excel(self.file_path)

        sys.exit("Only CSV and Excel files are supported")

    def get_cols(self):
        """Returns the columns found in the input file

        Args:
            None

        Returns:
            (`list` of `str`): column names of dataframe
        """
        return list(self.df)

    def set_col(self, column):
        """Set the date column to be parsed

        Args:
            column (`str`): column name

        Returns:
            None
        """

        if column in self.get_cols():
            self.column = column

        else:
            possible_cols = ", ".join(
                [col for col in list(self.df) if "date" in col.lower()]
            )

            sys.exit(
                dedent(
                    ("Inputted column ({wrong_col}) does not exist.\n"
                     "Possible date columns are:\n"
                     "{cols}".format(
                         wrong_col=self.column,
                         cols=possible_cols
                     )
                     )
                )
            )

    def clean_date_col(self):
        """Parses and standardizes the selected column values

        Args:
            None

        Returns:
            None
        """

        if self.column:

            self.df["tidy_date"] = self.df[self.column].apply(
                lambda x: self.parse_date(x)
            )

            self.df["tidy_date"] = self.df["tidy_date"].apply(
                lambda x: x.date() if notnull(x) else x
            )

    def split_date(self):
        """Splits the "tidy_date" column into separate tidy year, month and
        day columns

        Args:
            None

        Returns:
            None
        """

        for index, col in enumerate(self.tidy_date_split):

            self.df[col] = self.df["tidy_date"].apply(
                lambda x: int(str(x).split("-")[index]) if notnull(x) else x
            )

    def fill_na(self):
        """Fills values that were unable to be parsed with the original values

        Args:
            None

        Returns:
            None
        """

        self.tidy_date_split.append("tidy_date")

        for col in self.tidy_date_split:
            self.df[col].fillna(self.df[self.column], inplace=True)

    def download(self):
        """Initializes the parsing and cleaning procedure, and then saves the
        dataframe as a CSV file

        Args:
            None

        Returns:
            `True` if file was created successfully
        """

        self.clean_date_col()
        self.split_date()
        self.fill_na()

        new_file = self.file_name + "_tidydate.csv"

        self.df.to_csv(new_file, index=False)

        return False in set(
            np_where(
                self.df[self.column] == self.df["tidy_date"],
                True, False
            )
        )

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

import pandas as pd
import numpy as np

from .settings import VALID_COLS
from .tidytools import TidyDate, TidyBlockNLot


class TidyStar(object):

    def __init__(self, file_path, options=VALID_COLS, debug=False):
        """Constructs a TidyStar object by creating a dataframe from the input
        file

        Args:
            file_path (`str`): path of the uploaded dataset

        Returns:
            None
        """

        self.file_path = file_path
        self.options = options
        self.file_name = ""

        self.df = self.to_df()
        self.column = {}

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
            return pd.read_csv(self.file_path)

        elif ext == "xlsx":
            return pd.read_excel(self.file_path)

        sys.exit("Only CSV and Excel files are supported")

    def get_cols(self):
        """Returns the columns found in the input file

        Args:
            None

        Returns:
            (`list` of `str`): column names of dataframe
        """
        return set(self.df)

    def set_col(self, column):
        """Set the date column to be parsed

        Args:
            column (`str`): column name

        Returns:
            None
        """

        if len(set(column.values()) & self.get_cols()) \
                == len(set(column.values())):
            self.column = column

        else:
            possible_cols = ", ".join(
                [col for col in list(self.df) if any(
                    x in col.lower() for x in VALID_COLS)]
            )

            sys.exit(
                dedent(
                    ("Inputted columns ({wrong_col}) do not exist.\n"
                     "Possible columns are:\n"
                     "{cols}".format(
                         wrong_col=", ".join(column.values()),
                         cols=possible_cols
                     )
                     )
                )
            )

    def set_options(self):

        if "date" in self.options:
            tidydate_obj = TidyDate(self.df, self.column["date"])
            self.df = tidydate_obj.parse()

        if "blocknlot" in self.options:

            blocknlot_col = {}
            for key, value in self.column.items():
                if key != "date":
                    blocknlot_col[key] = value

            tidyblocknlot_obj = TidyBlockNLot(self.df, blocknlot_col)
            self.df = tidyblocknlot_obj.parse()

    def download(self):
        """Initializes the parsing and cleaning procedure, and then saves the
        dataframe as a CSV file

        Args:
            None

        Returns:
            `True` if file was created successfully
        """

        self.set_options()

        new_file = self.file_name + "_tidydate.csv"

        self.df.to_csv(new_file, encoding="utf-8", index=False)

        match_sets = []
        for key, value in self.column.items():
            match_sets.append(key)
            match_sets.append(
                set(
                    np.where(
                        self.df[value] == self.df["tidy_" + key],
                        True, False
                    )
                )
            )

        print(match_sets)
        # l
        return {True} not in match_sets

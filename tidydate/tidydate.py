from __future__ import absolute_import, print_function, unicode_literals

import sys
from textwrap import dedent

import dateparser
from pandas import notnull, read_csv, read_excel


class TidyDate(object):

    def __init__(self, file_path, col_name):

        self.file_name, self.df = self.to_df(file_path)
        self.col_name = col_name
        self.date_col = self.grab_date_col()
        self.clean_col = []
        self.tidy_date_split = [
            "tidy_year",
            "tidy_month",
            "tidy_day"
        ]

    @staticmethod
    def to_df(file_path):

        file_name, ext = file_path.split('.')

        if ext == "csv":
            return file_name, read_csv(file_path, index=False)

        elif ext == "xlsx":
            return file_name, read_excel(file_path, index=False)

    def grab_date_col(self):

        if self.col_name in list(self.df):
            return list(self.df[self.col_name])

        possible_cols = ", ".join(
            [col for col in list(self.df) if "date" in col.lower()]
        )

        sys.exit(
            dedent(
                ("Inputted column ({wrong_col}) does not exist.\n"
                 "Possible date columns are:\n"
                 "{cols}".format(
                     wrong_col=self.col_name,
                     cols=possible_cols
                 )
                 )
            )
        )

    def clean_date_col(self):

        if self.date_col:

            self.df["tidy_date"] = self.df[self.col_name].apply(
                lambda x: dateparser.parse(x)
            )

            self.df["tidy_date"] = self.df["tidy_date"].apply(
                lambda x: x.date() if notnull(x) else x
            )

    def split_date(self):

        for index, col in enumerate(self.tidy_date_split):

            self.df[col] = self.df["tidy_date"].apply(
                lambda x: int(str(x).split("-")[index]) if notnull(x) else x
            )

    def fill_na(self):

        self.tidy_date_split.append("tidy_date")

        for col in self.tidy_date_split:
            self.df[col].fillna(self.df[self.col_name], inplace=True)

    def download(self):

        self.clean_date_col()
        self.split_date()
        self.fill_na()
        self.df.to_csv(self.file_name + "_tidydate.csv", index=False)

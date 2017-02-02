from __future__ import absolute_import, print_function, unicode_literals

import sys
from textwrap import dedent

import dateparser
from pandas import notnull, read_csv, read_excel


class TidyDate(object):

    def __init__(self, file_path, col_name):

        self.df = self.file_type(file_path)
        self.col_name = col_name
        self.date_col = self.grab_date_col()
        self.clean_col = []

    @staticmethod
    def file_type(file_path):

        ext = file_path.split('.')[-1]

        if ext == "csv":
            return read_csv(file_path, index=False)

        elif ext == "xlsx":
            return read_excel(file_path, index=False)

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

            return self.df


if __name__ == '__main__':

    obj = TidyDate("nsnextract.xlsx", "Messy Date")
    obj.clean_date_col()

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

        # tidy_dates = list(self.df["tidy_date"])

        # tidy_year = []
        # tidy_month = []
        # tidy_day = []

        # for date in tidy_dates:
        #     try:
        #         year, month, day = date.split('-')
        #         tidy_year.append(year)
        #         tidy_month.append(month)
        #         tidy_day.append(day)

        #     except AttributeError:
        #         tidy_year.append("")
        #         tidy_month.append("")
        #         tidy_day.append("")
        #         continue

        # self.df["tidy_year"], self.df["tidy_month"], self.df["tidy_day"] = \
        #     tidy_year, tidy_month, tidy_day

        self.df["tidy_year"] = self.df["tidy_date"].apply(
            lambda x: str(x).split("-")[0] if notnull(x) else x
        )

        self.df["tidy_month"] = self.df["tidy_date"].apply(
            lambda x: str(x).split("-")[1] if notnull(x) else x
        )

        self.df["tidy_day"] = self.df["tidy_date"].apply(
            lambda x: str(x).split("-")[2] if notnull(x) else x
        )

    def fill_na(self):

        self.df["tidy_date"].fillna(self.df[self.col_name], inplace=True)
        self.df["tidy_year"].fillna(self.df[self.col_name], inplace=True)
        self.df["tidy_month"].fillna(self.df[self.col_name], inplace=True)
        self.df["tidy_day"].fillna(self.df[self.col_name], inplace=True)

        print(self.df)

    def download(self):

        self.clean_date_col()
        self.split_date()
        self.fill_na()
        self.df.to_csv(self.file_name + "_tidydate.csv", index=False)


if __name__ == '__main__':

    obj = TidyDate("nsnextract.xlsx", "Messy Date")
    obj.download()

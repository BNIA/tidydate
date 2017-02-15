#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

"""test_tidydate

"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path

from .context import modules
from modules import tidydate

FILE_CSV = "test_csv.csv"
FILE_XLSX = "test_xlsx.xlsx"
VALID_COL = "Messy Date"
INVALID_COL = "Title"

csv_obj = tidydate.TidyDate(FILE_CSV, debug=True)
xlsx_obj = tidydate.TidyDate(FILE_XLSX, debug=True)


def test_csv_valid():
    """CSV file with valid column selected"""

    csv_obj.set_col(VALID_COL)

    assert(csv_obj.download())


def test_csv_invalid():
    """CSV file with invalid column selected"""

    csv_obj.set_col(INVALID_COL)

    assert(not csv_obj.download())


def test_xlsx_valid():
    """Excel file with valid column selected"""

    xlsx_obj.set_col(VALID_COL)

    assert(xlsx_obj.download())


def test_xlsx_invalid():
    """Excel file with invalid column selected"""

    xlsx_obj.set_col(INVALID_COL)

    assert(not xlsx_obj.download())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_tidydate

Tests for server-side modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path

from .context import modules  # pylint: disable=unused-import
from modules import tidystar

SAMPLE_DIR = "samples"
FILE_CSV = path.join(SAMPLE_DIR, "test_csv.csv")
FILE_XLSX = path.join(SAMPLE_DIR, "test_xlsx.xlsx")

ALL_OPTS = [
    "date",
    "blocknlot"
]

VALID_COL = {
    "date": "Recv_Date",
    "block": "Block",
    "lot": "Lot"
}

INVALID_COL = {
    "date": "Case_Nbr",
    "block": "Case_Nbr",
    "lot": "Case_Nbr"
}

DNE_COL = {
    "date": "Meaning of life",
    "block": "Meaning of life",
    "lot": "Meaning of life"
}

csv_obj = tidystar.TidyStar(FILE_CSV, debug=True)
xlsx_obj = tidystar.TidyStar(FILE_XLSX, debug=True)


def test_csv_valid():
    """CSV file with valid column selected"""

    csv_obj.set_col(VALID_COL)
    csv_obj.set_opt(ALL_OPTS)

    assert(csv_obj.download())


def test_csv_invalid():
    """CSV file with invalid column selected"""

    csv_obj.set_col(INVALID_COL)
    csv_obj.set_opt(ALL_OPTS)

    assert(not csv_obj.download())


def test_xlsx_valid():
    """Excel file with valid column selected"""

    xlsx_obj.set_col(VALID_COL)
    xlsx_obj.set_opt(ALL_OPTS)

    assert(xlsx_obj.download())


def test_xlsx_invalid():
    """Excel file with invalid column selected"""

    xlsx_obj.set_col(INVALID_COL)
    xlsx_obj.set_opt(ALL_OPTS)

    assert(not xlsx_obj.download())


def test_xlsx_missing():
    """Excel file with non-existent column selected"""

    try:
        xlsx_obj.set_col(DNE_COL)
        xlsx_obj.set_opt(ALL_OPTS)

    except SystemExit:
        assert(not xlsx_obj.download())

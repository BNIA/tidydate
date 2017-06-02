#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_tidydate

Tests for server-side modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from ast import literal_eval
from sys import version_info
if version_info < (3, 0):
    from StringIO import StringIO as fileIO

else:
    from io import BytesIO as fileIO

from ..src.frontend.views import app
from . import FILE_CSV

app.debug = True
app_client = app.test_client()
app_client.testing = True


def test_index_status_code():
    """Sends HTTP GET request to the index path"""

    result = app_client.get("/")

    # assert the status code of the response
    assert(result.status_code == 200)


def test_upload():
    """POST requests with file uploads"""

    csv_data = ""

    with open(FILE_CSV, "rb") as csv_file:
        csv_data = csv_file.read()

    def format_response(response):

        return response.decode("utf-8") if version_info >= (3, 0) else response

    response = app_client.post(
        "/upload", buffered=True,
        content_type="multipart/form-data",
        data={"file": (fileIO(csv_data), "test_csv.csv")}
    )

    literal_response = literal_eval(
        format_response(
            response.data
        ).replace("\n", "").replace("false", "False").replace("true", "True")
    )

    assert(literal_response["received"])

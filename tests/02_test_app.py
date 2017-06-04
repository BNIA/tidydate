#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_tidydate

Tests for client-side modules
"""

from ast import literal_eval
from sys import version_info
if version_info < (3, 0):
    from StringIO import StringIO as file_io

else:
    from io import BytesIO as file_io

from . import FILE_CSV
from frontend.views import app

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
        data={"file": (file_io(csv_data), "test_csv.csv")}
    )

    literal_response = literal_eval(
        format_response(
            response.data
        ).replace("\n", "").replace("false", "False").replace("true", "True")
    )

    assert(literal_response["received"])

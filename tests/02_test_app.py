#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_tidydate

Tests for server-side modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from StringIO import StringIO
from ast import literal_eval

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

    with open(FILE_CSV) as csv_file:
        csv_data = csv_file.read()

    response = app_client.post(
        "/upload", buffered=True,
        content_type="multipart/form-data",
        data={"file": (StringIO(csv_data), "test_csv.csv")}
    )

    literal_response = literal_eval(
        response.data.replace("\n", "")
        .replace("false", "False").replace("true", "True")
    )

    assert(literal_response["received"])

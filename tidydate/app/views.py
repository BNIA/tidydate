#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

"""views

This file contains the endpoints for rendering the interface and implementing
the backend modules
"""

from os import path

from sanic.response import json

from .config import allowed_file, app, render_template, UPLOAD_FOLDER
from .context import modules
from modules import tidydate


@app.route('/')
async def test(request):
    data = {'name': 'name'}

    return render_template("index.html", name=data["name"])


@app.route('/upload', methods=["GET", "POST"])
async def upload(request):
    """Handles the uploaded file

    Args:
        None

    Returns:
        if POST: redirect here
        if GET: pass path of downloaded file on to be parsed
    """

    if request.method == 'POST':

        file = request.files.get("file")

        if file and allowed_file(file.name):

            app.file_name = file.name

            with open(
                path.join(UPLOAD_FOLDER, app.file_name), 'wb'
            ) as upload_file:
                upload_file.write(file.body)

            return json({"received": True, "file_names": file.name})

    app.df = tidydate.TidyDate(path.join(UPLOAD_FOLDER, app.file_name))

    return parse_date(request, app.file_name)


@app.route('/parse', methods=["GET", "POST"])
def parse_date(request, file_name):
    """Parses the uploaded file

    Args:
        file_name (`str`): path of the uploaded file

    Returns:
        if POST: (`str`): status of parsing file
        if GET: (`list` of `str`): list of column names in file
    """

    if request.method == "POST":

        column = request.form["column"][0]
        app.df.set_col(column)

        status_payload = "success" if app.df.download() else "failed"

        return json({"status": status_payload})

    return render_template("columns.html", columns=app.df.get_cols())

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
async def index(request):
    """Renders the index

    Args:
        None

    Returns:
        rendered template of "index.html"
    """
    return render_template("index.html")


@app.route('/upload', methods=["GET", "POST"])
async def upload(request):
    """Handles the uploaded file

    Args:
        None

    Returns:
        if POST: return upload success response
    """

    if request.method == 'POST':

        file = request.files.get("file")

        if file and allowed_file(file.name):

            app.file_name = file.name

            with open(
                path.join(UPLOAD_FOLDER, app.file_name), 'wb'
            ) as upload_file:
                upload_file.write(file.body)
            app.df = tidydate.TidyDate(path.join(UPLOAD_FOLDER, app.file_name))

            return json({"received": True, "file_names": file.name})


@app.route('/<file_name>', methods=["GET", "POST"])
async def parse_date(request, file_name):
    """Parses the uploaded file

    Args:
        file_name (`str`): path of the uploaded file

    Returns:
        if POST: (`str`): status of parsing file
        if GET: (`list` of `str`): list of column names in file in rendered
                template of "columns.html"
    """

    if request.method == "POST":
        column = request.form["column"][0]
        app.df.set_col(column)

        status_payload = "success" if app.df.download() else "failed"

        return json({"status": status_payload})

    return render_template("columns.html", columns=app.df.get_cols())


@app.route('/exit')
async def shutdown(request):
    """TODO: figure out how to safely shut server down"""
    raise KeyboardInterrupt

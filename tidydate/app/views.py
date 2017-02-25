#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""views

This file contains the endpoints for rendering the interface and implementing
the backend modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path

from flask import jsonify, render_template, request
from werkzeug import secure_filename

from .config import allowed_file, app, UPLOAD_FOLDER
from .context import modules  # pylint: disable=unused-import
from modules import tidydate


@app.route('/')
def index():
    """Renders the index

    Args:
        None

    Returns:
        rendered template of "index.html"
    """
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handles the uploaded file

    Args:
        None

    Returns:
        if POST: return upload success response
    """

    if request.method == "POST":

        file = request.files["file"]

        if file and allowed_file(file.filename):

            app.file_name = secure_filename(file.filename)
            file.save(path.join(UPLOAD_FOLDER, app.file_name))

            app.df = tidydate.TidyDate(path.join(UPLOAD_FOLDER, app.file_name))

            response = {"received": True, "file_name": app.file_name}

            print(response)
            return jsonify(response)


@app.route("/<file_name>", methods=["GET", "POST"])
def parse_date(file_name):
    """Parses the uploaded file

    Args:
        file_name (`str`): path of the uploaded file

    Returns:
        if POST: (`str`): status of parsing file
        if GET: (`list` of `str`): list of column names in file in rendered
                template of "columns.html"
    """

    if request.method == "POST":
        column = request.form.to_dict()["column"]
        app.df.set_col(column)

        status_payload = "success" if app.df.download() else "failed"

        return render_template("status.html", status=status_payload)

    if app.df:
        return render_template("columns.html", columns=app.df.get_cols())

    return render_template("columns.html")


@app.route("/exit")
def shutdown():
    """Calls the destructor and shuts down server

    Args:
        None

    Returns:
        (`str`): Server shutdown message
    """

    # ensures the destructor is called before shutting down
    del app.df

    werkzeug_server = request.environ.get("werkzeug.server.shutdown")
    if not werkzeug_server:
        raise RuntimeError("Not running with the Werkzeug Server")

    werkzeug_server()

    return "Server shutting down..."

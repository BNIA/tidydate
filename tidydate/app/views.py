#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

"""views

This file contains the endpoints for rendering the interface and implementing
the backend modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path

from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename

from .config import allowed_file, app
from .context import modules
from modules import tidydate


@app.route('/')
def index():
    """Renders the index page

    Args:
        None

    Returns:
        (`obj`): rendered template
    """
    return render_template('index.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    """Handles the uploaded file

    Args:
        None

    Returns:
        if POST: redirect here
        if GET: pass path of downloaded file on to be parsed
    """

    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):

            app.file_name = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], app.file_name))

            return redirect(url_for("upload"))

    app.df = tidydate.TidyDate(
        path.join(app.config['UPLOAD_FOLDER'], app.file_name)
    )

    return redirect(url_for("parse_date", file_name=app.file_name))


@app.route('/upload/<file_name>', methods=["GET", "POST"])
def parse_date(file_name):
    """Parses the uploaded file

    Args:
        file_name (`str`): path of the uploaded file

    Returns:
        if POST: (`str`): status of parsing file
        if GET: (`list` of `str`): list of column names in file
    """

    if request.method == "POST":

        column = request.form.to_dict()["column"]
        app.df.set_col(column)

        return "DONE" if app.df.download() else "FAILED"

    return render_template("columns.html", columns=app.df.get_cols())

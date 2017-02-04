#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

from __future__ import absolute_import, print_function, unicode_literals
from os import path

from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename

from .config import allowed_file, app
from .context import modules
from modules import tidydate


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():

    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):

            app.file_name = secure_filename(file.filename)
            file_path = path.join(app.config['UPLOAD_FOLDER'], app.file_name)
            file.save(file_path)
            return redirect(url_for("upload"))

    return redirect(
        url_for("uploaded_file", file_name=app.file_name)
    )


@app.route('/upload/<file_name>', methods=["GET", "POST"])
def uploaded_file(file_name):

    new_df = tidydate.TidyDate(
        path.join(app.config['UPLOAD_FOLDER'], file_name)
    )

    if request.method == "POST":

        column = request.form.to_dict()["column"]
        new_df.set_col(column)

        return "DONE" if new_df.download() else "FAILED"

    return render_template("columns.html", columns=new_df.get_cols())

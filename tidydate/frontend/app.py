#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

# from __future__ import absolute_import, print_function, unicode_literals
from os import path

from flask import Flask, request, redirect, url_for, \
    send_from_directory, render_template
from werkzeug import secure_filename

from context import modules
from modules import tidydate


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(["csv", "xlsx"])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fbdsbfhdsbfhfdsf'
app.FILE_NAME = ""
app.COLUMN = ""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=["GET", "POST"])
def upload_file():

    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):

            app.FILE_NAME = secure_filename(file.filename)
            file_path = path.join(app.config['UPLOAD_FOLDER'], app.FILE_NAME)
            file.save(file_path)
            app.COLUMN = request.form.to_dict()["column"]
            return ''

    return redirect(
        url_for("uploaded_file", file_name=app.FILE_NAME, column=app.COLUMN)
    )


@app.route('/upload/<file_name>/<column>')
def uploaded_file(file_name, column):

    new_df = tidydate.TidyDate(UPLOAD_FOLDER + file_name, column)
    new_df.download()

    return "yoyoyooy"


if __name__ == '__main__':
    app.run(debug=True)

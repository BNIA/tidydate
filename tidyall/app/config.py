#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config

This file instantiates the Flask app and other configurations
"""

from __future__ import absolute_import, print_function, unicode_literals
import string
from random import SystemRandom, uniform

from flask import Flask

from .context import modules # pylint: disable=unused-import
from modules._version import __version__

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx"}

app = Flask(__name__)

app.secret_key = ''.join(
    SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(int(uniform(10, 20)))
)
app.df = None


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.context_processor
def inject_version():
    """Inserts version number into templates

    Args:
        None

    Returns:
        (`dict`): version number of project
    """
    return dict(ver=__version__)

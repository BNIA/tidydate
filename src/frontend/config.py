#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config

This file instantiates the Flask app and other configurations
"""

from __future__ import absolute_import, print_function, unicode_literals

from os import path

from . import app
from .extra_mods import *  # pylint: disable=unused-import
from modules._version import __version__

UPLOAD_FOLDER = path.join(
    path.dirname(path.dirname(path.abspath(__file__))), "uploads"
)
ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def allowed_file(file_name):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.context_processor
def inject_version():
    """Inserts version number into templates

    Args:
        None

    Returns:
        (`dict`): version number of project
    """
    return dict(ver=__version__)

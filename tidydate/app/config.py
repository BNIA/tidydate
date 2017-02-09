#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config

This file instantiates the Sanic app and other configurations
"""

import string
from random import SystemRandom, uniform

from jinja2 import Environment, PackageLoader
from sanic import Sanic
from sanic.response import html

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx"}

app = Sanic()
env = Environment(loader=PackageLoader('app', 'templates'))

app.secret_key = ''.join(
    SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(int(uniform(10, 20)))
)
app.df = None


def render_template(file_name, **kwargs):

    template = env.get_template(file_name)
    return html(template.render(kwargs))


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

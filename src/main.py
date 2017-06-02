#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main

This file serves as the driver for the program by initializing the Flask app
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path, makedirs
import webbrowser

from frontend import views

if __name__ == "__main__":

    port_file_name = "port.txt"

    if not path.exists(port_file_name):
        with open(port_file_name, "w") as port_file:
            port = ""
            while len(port) != 4:
                port = str(input("Insert port: "))
            port_file.write(port)

    if not path.exists(views.UPLOAD_FOLDER):
        makedirs(views.UPLOAD_FOLDER)

    with open(port_file_name) as port_file:

        port = port_file.read()
        webbrowser.get().open_new_tab(
            "http://localhost:{PORT}".format(PORT=port)
        )

        views.app.run(port=int(port))

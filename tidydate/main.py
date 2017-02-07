#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main

This file serves as the driver for the program by initializing the Sanic app
"""

from os import path
import webbrowser

from app import views

if __name__ == '__main__':

    port_file_name = "port.txt"

    from time import sleep

    def x():
        sleep(5)

    if not path.exists(port_file_name):
        with open(port_file_name, 'w') as port_file:
            port = ""
            while len(port) != 4:
                port = str(input("Insert port: "))
            port_file.write(port)

    with open(port_file_name) as port_file:

        port = port_file.read()
        # webbrowser.get().open_new_tab(
        #     "http://localhost:{PORT}".format(PORT=port)
        # )

        views.app.run(host="0.0.0.0", port=int(port), debug=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""make_spec

This module creates spec files for building production executable with
specific configuration for PyInstaller
"""

from __future__ import absolute_import, print_function, unicode_literals
from os import path
from sys import platform
from textwrap import dedent

SPEC_STR = """\
    # -*- mode: python -*-

    a = Analysis(
        ["{ROOT}{MOD_PATH}"],
        pathex=["{PROJ_PATH}"],
        binaries=None,
        datas=[
            ("{ROOT}src/{TEMPLATE_PATH}",
                "{TEMPLATE_PATH}")
        ],
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=None
    )

    pyz = PYZ(
        a.pure,
        a.zipped_data,
        cipher=None
    )

    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name="tidyall",
        debug=False,
        strip=False,
        upx=True,
        console=True,
        icon="{ROOT}{ICO_PATH}"
    )
"""

PROJ_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

spec_output = dedent(
    SPEC_STR.format(
        ROOT="../../",
        MOD_PATH=path.join("src", "main.py"),
        PROJ_PATH=PROJ_DIR,
        TEMPLATE_PATH=path.join("frontend", "templates"),
        ICO_PATH=path.join("src", "frontend", "static", "img", "logo.ico")
    )
)

if platform == "win32":
    for char in ['\\', '/']:
        spec_output = spec_output.replace(char, "\\\\")

if __name__ == '__main__':

    with open("tidyall.spec", "w") as spec_file:
        spec_file.write(spec_output)

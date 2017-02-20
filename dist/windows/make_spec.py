#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""make_spec

This module creates spec files for building production executable with
specific configuration for PyInstaller
"""

from __future__ import absolute_import, print_function, unicode_literals

if __name__ == '__main__':

    from os import path
    from sys import platform
    from textwrap import dedent

    SPEC_STR = """\
        # -*- mode: python -*-

        block_cipher = None

        a = Analysis(
            ["{ROOT}{MOD_PATH}"],
            pathex=["{PROJ_PATH}"],
            binaries=None,
            datas=[
                ("{ROOT}tidydate/{TEMPLATE_PATH}",
                    "{TEMPLATE_PATH}")
            ],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher
        )

        pyz = PYZ(
            a.pure,
            a.zipped_data,
            cipher=block_cipher
        )

        exe = EXE(
            pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name="tidydate",
            debug=False,
            strip=False,
            upx=True,
            console=True,
            # icon="{ROOT}{ICO_PATH}"
        )
    """

    PROJ_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    spec_output = dedent(
        SPEC_STR.format(
            ROOT="../../",
            MOD_PATH=path.join("tidydate", "main.py"),
            PROJ_PATH=PROJ_DIR,
            TEMPLATE_PATH=path.join("app", "templates"),
            ICO_PATH=path.join(
                "tidydate", "app", "static", "img", "logo.ico")
        )
    )

    if platform == "win32":
        for char in ['\\', '/']:
            spec_output = spec_output.replace(char, "\\\\")

    with open("tidydate.spec", "w") as spec_file:
        spec_file.write(spec_output)

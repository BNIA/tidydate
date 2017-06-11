# -*- mode: python -*-

a = Analysis(
    ["../../src/main.py"],
    pathex=["/home/sabbir/Desktop/BNIA/tidyall"],
    binaries=None,
    datas=[
        ("../../src/frontend/templates",
            "frontend/templates")
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
    debug=True,
    strip=False,
    upx=True,
    console=True,
    icon="../../src/frontend/static/img/logo.ico"
)

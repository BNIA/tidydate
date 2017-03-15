# -*- mode: python -*-

a = Analysis(
    ["..\\..\\tidyall\\main.py"],
    pathex=["C:\\Users\\sabbi\\Documents\\GitHub\\tidydate"],
    binaries=None,
    datas=[
        ("..\\..\\tidyall\\app\\templates",
            "app\\templates")
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
    # icon="..\\..\\tidyall\\app\\static\\img\\logo.ico"
)

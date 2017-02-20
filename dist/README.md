# Production

A single Windows executable file is compiled as the final product.

## Build

[PyInstaller](http://www.pyinstaller.org/) was used to build the Windows executable. The spec file is used for the configuration of the build.

Spec file configurations depend on the local systems. To build a spec file, run `make_spec.py`

To build, run `pyinstaller tidydate.spec`

## System dependancies

The Windows executable was built in a win32 environment on Windows 10, and has been tested against Windows 10 systems, and Windows XP, Windows 7 and Windows 8 virtual environments. Linux executables were also created and tested against during development.

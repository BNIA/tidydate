<div align="center">
  <img src="https://raw.githubusercontent.com/BNIA/tidyall/master/tidyall/app/static/img/logo.png" width="50%">
</div>


[![Build Status](https://travis-ci.org/BNIA/tidyall.svg?branch=master)](https://travis-ci.org/BNIA/tidyall)

A tool for parsing and standardizing unstructured date columns into ISO 8601 formats.


## Interface

TidyDate is a standalone Flask app with a web application interface. The minimalistic templates allow the user to drag and drop (or manually) upload the Excel or CSV dataset, choose the date column to be parsed, and download the new dataset as a CSV file.

Usage of the interface is detailed [here](https://github.com/BNIA/tidydate/docs/usage.md).


## Modules

python-dateutils is used for parsing the various date formats and pandas and numpy is used for manipulating dataframes.


## Installation

### Production

A standalone executable can be found in the dist directory. The executable was created on a Windows 10 system, and has been tested against Windows 10 systems, and Windows XP, Windows 7 and Windows 8 virtual environments.


### Development

If you are not familiar with Python projects on Windows machines, you might want to check out [this quick guide](https://github.com/BNIA/Close-Crawl/blob/master/docs/windows-dev-setup.md).

#### Requirements

- Python 2.7, 3.5
- Packages in `requirements.txt`

Clone the repository, create a virtual environment and install the packages via pip: `pip install -r requirements.txt`.<br>
Or run the Makefile: `make install`

#### Tests

The tests run on [nose](http://nose.readthedocs.io/en/latest/). To install, run: `pip install nose`
- For UNIX machines, a Makefile has been provided for convenience. Just run: `make test`
- For non-UNIX machines: `nosetests -v -w tests` will work.

#### Executable

[PyInstaller](http://www.pyinstaller.org/) was used to build the Windows executable. More details on the building process can be found [here](https://github.com/BNIA/tidydate/blob/master/dist/README.md)

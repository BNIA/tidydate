# Makefile to ease trivial tasks for the project

VENV="$(shell find . -name ".*env")"
IN_VENV="$(shell python env.py)"
REQ=requirements.txt


.PHONY: clean
clean:
	# clean out cache and temporary files
	@find . \( -name "*.pyc" -o -name "port.txt"  -o \
		-name "*_tidydate.csv" \) -type f -delete
	@find . -name "__pycache__" -type d -delete


.PHONY: install
install:
	# install the virtual environment
	@test -d $(VENV) && virtualenv $(VENV) || virtualenv .venv


.PHONY: upgrade
upgrade:
	# upgrade PIP on virtual environment
	@test 1 -eq $(IN_VENV) && pip install -U pip && pip install -r $(REQ) \
	|| echo 'Activate virtual environment first'


.PHONY: update
update:
	# update PIP requirements
	@test 1 -eq $(IN_VENV) && pip freeze | grep -Ev "PyInstaller|nose" > $(REQ) \
	|| echo 'Activate virtual environment first'


.PHONY: test
test:
	# run backend unit tests
	@nosetests -v -w tests

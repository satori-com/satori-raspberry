PYTHON ?= python3
VIRTUALENV ?= virtualenv

DENV = denv
ABS_DENV = $(abspath ${DENV})
DENV_BIN = ${ABS_DENV}/bin

PIP ?= ${DENV_BIN}/pip

${DENV}:
	$(VIRTUALENV) ${DENV} --python=${PYTHON}
	PYTHON_PREFIX=${DENV_BIN}/ ${PIP} install -r requirements.txt
	@echo "Use 'make run' to run the application"

dev: ${DENV}
	PYTHON_PREFIX=${DENV_BIN}/ ${PIP} install -r requirements-dev.txt

run: ${DENV}
	PYTHON_PREFIX=${DENV_BIN}/ ${DENV_BIN}/python3 rsb-satori/app.py config.json

clean:
	rm -rf ${ABS_DENV} build

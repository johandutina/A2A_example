#.ONESHELL:
SHELL:=/bin/bash
VENV_ACTIVATE=source ${VENV}/bin/activate
VENV=.venv
PYTHON=3.9
COMMAND?=
PROFILE?=--profiles-dir .profiles

setup: _setup_venv _install_modules

install_modules: _install_modules

info: _info

run: _run

test: _test

clean: _clean

_setup_venv:
	( \
	rm -fr ${VENV} ;\
	python${PYTHON} -m venv ${VENV} ;\
	)

_info:
	( \
	$(VENV_ACTIVATE) ;\
	echo "PIP INFO" ;\
	which pip ;\
	pip --version ;\
	python${PYTHON} -m pip list ;\
	echo "PYTHON INFO" ;\
	which python${PYTHON} ;\
	python${PYTHON} --version ;\
	)

_install_modules:
	( \
	$(VENV_ACTIVATE) ;\
	python${PYTHON} -m pip install --upgrade pip ;\
	python${PYTHON} -m pip install -r requirements.txt ;\
	which pip ;\
	which python${PYTHON} ;\
	python${PYTHON} -m pip list ;\
	python${PYTHON} --version ;\
	pip --version ;\
	)

_run:
	( \
	$(VENV_ACTIVATE) ;\
	cd agent ;\
	uvicorn code_generator_agent:app --reload ;\
	)

_clean:
	( \
	rm -fr ${VENV} ;\
	)



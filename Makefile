# Makefile for RSUV3.
#
# Source:: https://github.com/ampledata/rsuv3
# Author:: Greg Albrecht W2GMD <oss@undef.net>
# Copyright:: Copyright 2017 Greg Albrecht
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: develop

develop: remember
	python setup.py develop

install: remember
	python setup.py install

install_requirements:
	pip install -r requirements.txt

uninstall:
	pip uninstall -y rsuv3

reinstall: uninstall install

remember:
	@echo
	@echo "Hello from the Makefile..."
	@echo "Don't forget to run: 'make install_requirements'"
	@echo

clean:
	@rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log .coverage

publish: remember
	python setup.py register sdist upload

nosetests: remember
	python setup.py nosetests

pep8: remember
	flake8 --max-complexity 12 --exit-zero rsuv3/*.py tests/*.py *.py

flake8: pep8

lint: remember
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
	-r n *.py  --ignore-imports=y rsuv3/*.py tests/*.py || exit 0

pylint: lint

clonedigger: remember
	clonedigger --cpd-output .

coverage:
	coverage report -m

test: lint flake8 nosetests coverage

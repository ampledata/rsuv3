# Makefile for RSUV3.
#
# Source:: https://github.com/ampledata/rsuv3
# Author:: Greg Albrecht W2GMD <gba@orionlabs.io>
# Copyright:: Copyright 2016 Orion Labs, Inc.
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: install_requirements develop

develop:
	python setup.py develop

install:
	python setup.py install

install_requirements:
	pip install --upgrade -r requirements.txt

uninstall:
	pip uninstall -y rsuv3

reinstall: uninstall install

clean:
	rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log *.egg output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log *.deb *.eggs

clonedigger:
	clonedigger --cpd-output .

publish:
	python setup.py register sdist upload

nosetests:
	python setup.py nosetests

pep8:
	flake8

flake8: install_requirements
	flake8 --max-complexity 12 --exit-zero rsuv3/*.py tests/*.py *.py

lint: install_requirements
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
	-r n rsuv3/*.py tests/*.py *.py || exit 0

test: lint flake8 nosetests

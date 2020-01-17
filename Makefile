help:
	cat Makefile

test:
	python3.6 -m pytest --benchmark-disable --showlocals
	python2.7 -m pytest --benchmark-disable --showlocals
	pypy      -m pytest --benchmark-disable --showlocals

verbose:
	python3.6 -m pytest --benchmark-disable --showlocals --verbose
	python2.7 -m pytest --benchmark-disable --showlocals --verbose
	pypy      -m pytest --benchmark-disable --showlocals --verbose

xfails:
	python3.6 -m pytest --benchmark-disable --verbose | egrep --color=always "xfail|XFAIL|xpass|XPASS"
	python2.7 -m pytest --benchmark-disable --verbose | egrep --color=always "xfail|XFAIL|xpass|XPASS"
	pypy      -m pytest --benchmark-disable --verbose | egrep --color=always "xfail|XFAIL|xpass|XPASS"

cover:
	python3.6 -m pytest --benchmark-disable --cov construct --cov-report html --cov-report term --verbose

bench:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare

benchsave:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare --benchmark-autosave

html:
	cd docs; make html

installdeps:
	apt-get install python3.6 python2.7 pypy python3-sphinx --upgrade
	python3.6 -m pip install pytest pytest-benchmark pytest-cov enum34 numpy arrow ruamel.yaml --upgrade
	python2.7 -m pip install pytest pytest-benchmark pytest-cov enum34 numpy arrow ruamel.yaml --upgrade
	pypy      -m pip install pytest pytest-benchmark pytest-cov enum34       arrow             --upgrade

version:
	./version-increment

upload:
	./setup.py sdist
	python3 -m twine upload dist/*


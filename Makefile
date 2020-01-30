help:
	cat Makefile

test:
	python3.6 -m pytest --benchmark-disable --showlocals

verbose:
	python3.6 -m pytest --benchmark-disable --showlocals --verbose

xfails:
	python3.6 -m pytest --benchmark-disable --verbose | egrep --color=always "xfail|XFAIL|xpass|XPASS"

cover:
	python3.6 -m pytest --benchmark-disable --cov construct --cov-report html --cov-report term --verbose

bench:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare

benchsave:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare --benchmark-autosave

html:
	cd docs; make html

installdeps:
	apt-get install python3.6 python3-sphinx --upgrade
	python3.6 -m pip install pytest pytest-benchmark pytest-cov twine --upgrade
	python3.6 -m pip install enum34 numpy arrow ruamel.yaml --upgrade

version:
	./version-increment

upload:
	python3.6 ./setup.py sdist
	python3.6 -m twine upload dist/*


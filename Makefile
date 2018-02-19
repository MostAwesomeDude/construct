test:
	python3.6 -m pytest --benchmark-disable --showlocals
	python2.7 -m pytest --benchmark-disable --showlocals
	pypy      -m pytest --benchmark-disable --showlocals

verbose:
	python3.6 -m pytest --benchmark-disable --fulltrace --showlocals --verbose
	python2.7 -m pytest --benchmark-disable --fulltrace --showlocals --verbose
	pypy      -m pytest --benchmark-disable --fulltrace --showlocals --verbose

cover:
	python3.6 -m pytest --benchmark-disable --cov construct --cov-report html --cov-report term --verbose

bench:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare

benchsave:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,stddev --benchmark-sort=name --benchmark-compare --benchmark-autosave

installdeps:
	apt-get install python3.6 python2.7 pypy --upgrade
	python3.6 -m pip install pytest pytest-benchmark pytest-cov enum34 numpy arrow --upgrade
	python2.7 -m pip install pytest pytest-benchmark            enum34 numpy arrow --upgrade
	pypy      -m pip install pytest pytest-benchmark            enum34       arrow --upgrade

version:
	./version-increment

upload:
	./setup.py sdist upload

test:
	python3.6 -m pytest --benchmark-disable --showlocals
	python2.7 -m pytest --benchmark-skip    --showlocals
	pypy -m pytest      --benchmark-skip    --showlocals

verbose:
	python3.6 -m pytest --benchmark-disable --fulltrace --showlocals --verbose
	python2.7 -m pytest --benchmark-skip    --fulltrace --showlocals --verbose
	pypy -m pytest      --benchmark-skip    --fulltrace --showlocals --verbose

cover:
	python3.6 -m pytest --benchmark-disable --cov {envsitepackagesdir}/construct --cov-report html --cov-report term --verbose

bench:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,max,mean,stddev,median,rounds --benchmark-sort=name --benchmark-compare

benchsave:
	python3.6 -m pytest --benchmark-enable --benchmark-columns=min,max,mean,stddev,median,rounds --benchmark-sort=name --benchmark-autosave

installdeps:
	python3.6 -m pip install pytest pytest-benchmark pytest-cov enum34 numpy --upgrade
	python2.7 -m pip install pytest pytest-benchmark pytest-cov enum34 numpy --upgrade
	pypy      -m pip install pytest pytest-benchmark pytest-cov enum34 numpy --upgrade

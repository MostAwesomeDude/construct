#!/bin/sh
python setup.py register
python setup.py sdist --formats=zip,gztar upload
python setup.py bdist_wininst --plat-name=win32 upload
# Make sure you have 'wheel' installed: pip install wheel
python setup.py bdist_wheel upload 

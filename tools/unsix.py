#!/usr/bin/python3

import re, os, sys

def processfolder(top): 
    for root, dirs, files in os.walk(top):
        for f in files:
            if f.endswith('.py'):
                processfile(os.path.join(root, f))
        for d in dirs:
            processfolder(os.path.join(root, d))

def processfile(fname):
    print(fname+'... ', end='')
    with open(fname, 'rt') as f:
        txt = f.read()
    txt = re.sub('import six\n', '', txt)
    txt = re.sub(r'six\.(b\("[^"]*"\))', 
        lambda s: 'b'+s.expand(r'\1').strip('b()'), txt)
    txt = re.sub(r'six\.(u\("[^"]*"\))', 
        lambda s: 'u'+s.expand(r'\1').strip('u()'), txt)
    with open(fname, 'wt') as f:
        f.write(txt)
    print('done')


processfolder(sys.argv[1])

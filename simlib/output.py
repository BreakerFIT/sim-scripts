
from __future__ import print_function
import errno
import os
import os.path
import re
import sys

logfile = None

def unbuffer_stdout():
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class tee_file:
    def __init__(self, _file1, _file2) :
        self.file1 = _file1
        self.file2 = _file2

    def __del__(self) :
        if self.file1 != sys.stdout and self.file1 != sys.stderr :
            self.file1.close()
        if self.file2 != sys.stdout and self.file2 != sys.stderr :
            self.file2.close()

    def write(self, text) :
        self.file1.write(text)
        self.file2.write(text)

    def flush(self) :
        self.file1.flush()
        self.file2.flush()

def tee_output(outfile):
    tee = tee_file(sys.stdout, outfile)
    sys.stdout = tee
    sys.stderr = tee

def prep_output(out_fname):
    unbuffer_stdout()
    mkdir_p('results')
    outfile = open('results/' + out_fname, 'w', 0)
    tee_output(outfile)

    log_fname = re.sub('-', '-log-', out_fname, count=1)

    global logfile
    logfile = open('results/' + log_fname, 'w', 0)

def log(str, newline=True):
    print(str, file=logfile, end='\n' if newline else '', sep='')

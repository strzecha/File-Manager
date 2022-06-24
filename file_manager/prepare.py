"""script prepare

Script to prepare testing two-level directory tree
"""
from utils import load_configuration, prepare_subfiles
from sys import argv

if len(argv) > 3:
    (_, b, _, t) = load_configuration(argv[2])
    prepare_subfiles(argv[1], b, t, int(argv[3]))
    print("Files created")
else:
    print("Too few arguments")

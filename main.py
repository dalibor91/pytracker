#!/usr/bin/python
import sqlite3
import hashlib
import os
import sys
import uuid

from pytracker import process_args

program = os.path.basename(sys.argv[0])

try:
    process_args(program, sys.argv[1:])
except Exception as e:
    print(str(e))
    sys.exit(1)

exit(0)

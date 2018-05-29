#!/usr/bin/env python

import os
import sys

from pytrack import process_args, help

program = os.path.basename(sys.argv[0])

try:
    process_args(program, sys.argv[1:])
except Exception as e:
    raise e
    print(str(e))
    help(program)
    sys.exit(1)

exit(0)

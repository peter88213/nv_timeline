#!/usr/bin/python3
"""Helper file for nv-timeline test.

Create config file.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw2xtg
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import os
from nvlib.configuration.configuration import Configuration
from yw_timeline_ import SETTINGS
from yw_timeline_ import OPTIONS
from yw_timeline_ import APPNAME


def run(iniFile):
    iniDir = os.path.dirname(iniFile)
    if not os.path.isdir(iniDir):
        os.makedirs(iniDir)
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.write(iniFile)
    print(f'{iniFile} written.')


if __name__ == '__main__':
    try:
        iniFile = sys.argv[1]
    except:
        iniFile = f'./{APPNAME}.ini'
    run(iniFile)

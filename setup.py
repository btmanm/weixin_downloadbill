# -*- coding: utf-8 -*-

import sys

from distutils.core import setup
import py2exe
 
sys.argv.append('py2exe')

setup(
    windows = ['main.py'],
)
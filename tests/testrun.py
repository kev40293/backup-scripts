#!/usr/bin/python
from sys import path
path.insert(0, '../src/')
import logging
logging.getLogger().setLevel("DEBUG")

import imp
imp.load_source('timeball', '../src/timeball')


#!/usr/bin/python
from sys import path
path.insert(0, '../')
import logging
logging.getLogger().setLevel(logging.DEBUG)

import imp
imp.load_source('timeball', '../timeball')


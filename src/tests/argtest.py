#!/usr/bin/python2.7
from sys import path
path.insert(0, '../src/')
import logging
logging.getLogger().setLevel("DEBUG")

from timeball_utils import argparser, configparser
from sys import argv

parsed = argparser.parse_cl(configparser.default_opts())

print parsed

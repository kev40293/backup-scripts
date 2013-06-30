#!/usr/bin/python2.7

import argparse
from sys import argv, exit

default_opts = {
      "name": None,
      "target": None,
      "dest": None,
      "exclude": [],
      "profile": "default",
      "log-level": "warning",
      "back_type": None,
      }
def parse_cl(options=default_opts):
   aparse = argparse.ArgumentParser(prog="timeball")

   if argv[1] == "backup":
      aparse.add_argument("target", nargs='?', default=options['target'])
      aparse.add_argument("dest", nargs='?', default=options['dest'])
      aparse.add_argument("--name", default=options['name'])
      aparse.add_argument("--target", default=options['target'])
      aparse.add_argument("--dest", default=options['dest'])
      aparse.add_argument("--exclude", default=options['exclude'], action='append')
      aparse.add_argument("--log-level", default=options['log-level'])
      aparse.add_argument("--profile", default=options['profile'])
      aparse.add_argument("--full", action='store_const', dest='back_type', const="full")
      aparse.add_argument("--partial", action='store_const', dest='back_type', const="part")
   elif argv[1] == "delete":
      aparse.add_argument("target", default=options['target'])
   elif argv[1] == "recover":
      aparse.add_argument("target", default=options['target'])
      aparse.add_argument("dest", default=options['dest'])
   else:
      print "No valid action supplied"
      exit(1)
   return aparse.parse_args(argv[2:])

#!/usr/bin/python2.7

import argparse
from sys import exit, argv
import logging
general_usage = "usage: timeball <command> [<args>]\n" + "Available commands:\n" + "   backup      Perform a full or partial backup\n" + "   recover     Recover a backup\n" + "   delete      Delete a backup\n\n" + "See 'timeball <command> --help for command specific options"

log_levels = { "debug" : logging.DEBUG,
               "info" : logging.INFO,
               "warning" : logging.WARNING,
               "error" : logging.ERROR,
               "critical" : logging.CRITICAL
               }

default_opts = {
      "name": None,
      "target": None,
      "dest": None,
      "exclude": [],
      "profile": "default",
      "log-level": "warning",
      "back_type": None
      }
def parse_cl(cl_args, options=default_opts):
   aparse = argparse.ArgumentParser(prog="timeball")

   aparse.add_argument("--log-level", default=options['log-level'], choices=log_levels.keys())
   operation = None
   if cl_args:
       operation = cl_args.pop(0)
   if operation == "backup":
      aparse.add_argument("target", nargs='?', default=options['target'])
      aparse.add_argument("dest", nargs='?', default=options['dest'])
      aparse.add_argument("--name", default=options['name'])
      aparse.add_argument("--exclude", default=options['exclude'], action='append')
      aparse.add_argument("--profile", default=options['profile'])
      aparse.add_argument("--full", action='store_const', dest='back_type', const="full")
      aparse.add_argument("--partial", action='store_const', dest='back_type', const="part")
   elif operation == "delete":
      aparse.add_argument("backup-file")
   elif operation == "recover":
      aparse.add_argument("backup-file")
      aparse.add_argument("dest", default='.', nargs="?")
   else:
      print general_usage
      exit(0)
   options = vars(aparse.parse_args(cl_args))
   options['back_type'] = operation
   return options

import os
from configparser import config_parser
def get_options():
    opts = parse_cl(argv)
    cparse = config_parser(os.environ['HOME'] + "/.timeball")
    copts = cparse.get_options(profile=opts['profile'])
    if (opts['back_type'] == 'backup'):
        for var in ['target', 'dest']:
            if opts[var] == None:
                opts[var] = copts[var]
        for exc in copts['exclude']:
            opts['exclude'].append(exc)
    return opts

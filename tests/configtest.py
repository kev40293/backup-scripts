#!/usr/bin/python

import sys
sys.path.insert(0, '../src')
from timeball_utils.configparser import backup_parser, config_parser, arg_parser

def backup():
   cparse = backup_parser(sys.argv[2])
   backups = dict()
   while not cparse.empty():
      date = cparse.parseString()
      if date is None:
         break
      backup_list = cparse.parseBlock()
      if backup_list is None:
         break
      backups[date] = backup_list
   bparse = backup_parser(sys.argv[2])
   backups = bparse.read_backup_file()

   for key in backups.keys():
      print (key + " {\n")
      for v in backups[key]:
         print (v + "\n")
      print ("}\n")

   print max(backups.keys())


def config():
   cparse = config_parser(sys.argv[2])
   print cparse.get_opt("exclude")
   print cparse.get_opt("exclude", profile="kevin")
   print cparse.get_options(profile='vbox')
   aparse = arg_parser(sys.argv[1:], opt=cparse.get_options())
   aparse = arg_parser(sys.argv[1:])
   print aparse.options
   print aparse.options['exclude']
   print cparse.get_opt('name', profile='vbox')

if sys.argv[1] == 'config':
   config()
elif sys.argv[1] == 'backup':
   backup()
else:
   aparse = arg_parser(sys.argv[1:])
   print aparse.options

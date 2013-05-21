#!/usr/bin/python

from ptb_utils.configparser import backup_parser, config_parser, arg_parser
import sys

cparse = backup_parser(sys.argv[1])
backups = dict()
while not cparse.empty():
   date = cparse.parseString()
   if date is None:
      break
   backup_list = cparse.parseBlock()
   if backup_list is None:
      break
   backups[date] = backup_list
bparse = backup_parser(sys.argv[1])
backups = bparse.read_backup_file()

for key in backups.keys():
   print (key + " {\n")
   for v in backups[key]:
      print (v + "\n")
   print ("}\n")

print max(backups.keys())


#cparse = config_parser("example-config")
#print cparse.get_opt("exclude")
#print cparse.get_opt("exclude", profile="kevin")
#aparse = arg_parser(sys.argv[1:], opt=cparse.get_options())
#aparse = arg_parser(sys.argv[1:])
#print aparse.options
#print aparse.options['exclude']

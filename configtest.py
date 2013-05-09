#!/usr/bin/python

from configparser import backup_parser, config_parser
import sys

#cparse = parser(sys.argv[1])
#backups = dict()
#while not cparse.empty():
   #date = cparse.parseString()
   #if date is None:
      #break
   #backup_list = cparse.parseBlock()
   #if backup_list is None:
      #break
   #backups[date] = backup_list
#bparse = backup_parser(sys.argv[1])
#backups = bparse.read_backup_file()

#or key in backups.keys():
#   print (key + " {\n")
#   for v in backups[key]:
#      print (v + "\n")
#   print ("}\n")

options = dict()

cparse = config_parser("example-config")
print cparse.get_opt("exclude")
print cparse.get_opt("exclude", profile="kevin")

#!/usr/bin/python

from configparser import parser
import sys

cparse = parser(sys.argv[1])
backups = dict()
while not cparse.empty():
   date = cparse.parseString()
   if date is None:
      break
   backup_list = cparse.parseBlock()
   if backup_list is None:
      break
   backups[date] = backup_list

for key in backups.keys():
   print (key + " {\n")
   for v in backups[key]:
      print (v + "\n")
   print ("}\n")

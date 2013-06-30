#!/usr/bin/python
#      recover.py : handles the recovery of a backup
#      Copyright (C) 2013  Kevin Brandstatter <icarusthecow@gmail.com>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.


from configparser import backup_parser, usage
from version import notice
import sys, os
from subprocess import call
import logging

def run(args):
   if len(args) != 3:
      print usage
      sys.exit(1)

   print notice
   #formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')

   backup_file=os.path.realpath(args[1])
   backup_dir=os.path.dirname(backup_file)
   name="".join(os.path.basename(backup_file).split('.')[0:-1])

   destination=os.path.realpath(args[2])

   bparse = backup_parser(backup_file)
   recover_date = max(bparse.backups.keys())
   archives = bparse.backups[recover_date]

   oldcwd = os.getcwd()
   os.chdir(destination)
   dlist = generate_datelist(bparse.backups)
   for i,d in enumerate(dlist):
      print str(i) + ") " + d
   print ""
   sys.stdout.write( "Select a date to restore from (0): ")
   cin = sys.stdin.readline().rstrip('\n')
   if cin == "":
      choice = 0
   else:
      choice = int(cin)
   recover_date = dlist[choice]
   logging.debug(recover_date)

   sys.stdout.write("Restore from " + recover_date + " (y/N) ")
   cin = sys.stdin.readline().rstrip('\n')
   if cin != "y":
      return

   snarfile = backup_dir + "/" + name + '-' + recover_date + ".snar"
   base_back = None
   for k in bparse.backups.keys():
      if k <= recover_date:
         if base_back is None or base_back < k:
            base_back = k
   logging.debug("base_back " + base_back)
   archives = []
   for arc in bparse.backups[base_back]:
      logging.debug(arc)
      if strip_date(arc) <= recover_date:
         archives.append(arc)

   archives.sort()

   for arc in archives:
      tar_args = ['tar', '-xjvf', backup_dir +"/" + arc, '-g', snarfile]
      call(tar_args)

   os.chdir(oldcwd)

def strip_date(arcname):
   return "-".join(arcname.split('-')[-3:]).rstrip('.tar.bz2')

def generate_datelist(backupdb):
   datelist = []
   for key in backupdb.keys():
      for arc in backupdb[key]:
         date = strip_date(arc)
         datelist.append(date)
   datelist.sort()
   datelist.reverse()
   return datelist

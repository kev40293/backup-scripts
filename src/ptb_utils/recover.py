#!/usr/bin/python
#      recover.py : handles the recovery of a backup
#      Copyright (C) 2013  Kevin Brandstatter <icarusthecow@gmail.com>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.


from configparser import backup_parser
import sys, os
from subprocess import call

def run(args):
   if len(args) != 3:
      print "recover.py backup-file destination"
      sys.exit(1)

   backup_file=os.path.realpath(args[1])
   backup_dir=os.path.dirname(backup_file)
   name="".join(os.path.basename(backup_file).split('.')[0:-1])

   destination=os.path.realpath(args[2])

   bparse = backup_parser(backup_file)
   recover_date = max(bparse.backups.keys())
   archives = bparse.backups[recover_date]
   snarfile = backup_dir + "/" + recover_date + ".snar"

   oldcwd = os.getcwd()
   os.chdir(destination)

   for arc in archives:
      tar_args = ['tar', '-xjvf', backup_dir +"/" + arc, '-g', snarfile]
      call(tar_args)

   os.chdir(oldcwd)

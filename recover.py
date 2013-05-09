#!/usr/bin/python

from configparser import backup_parser
import sys, os
from subprocess import call

if len(sys.argv) != 3:
   print "recover.py backup-file destination"
   sys.exit(1)

backup_file=os.path.realpath(sys.argv[1])
backup_dir=os.path.dirname(backup_file)
name="".join(os.path.basename(backup_file).split('.')[0:-1])

destination=os.path.realpath(sys.argv[2])

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

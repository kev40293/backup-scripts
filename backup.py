#!/usr/bin/python

import sys
import os
import os.path
from subprocess import call
import datetime
from configparser import backup_parser


now= datetime.datetime.now()
curdate = now.strftime("%Y-%m-%dT%H:%M:%S")

class backup:
   def __init__(self):
      pass
   def __init__(self, path_to_target, destination, excludes=[], name=""):
      self.target = os.path.basename(path_to_target)
      self.dest = destination
      self.target_dir = os.path.dirname(path_to_target)
      self.exclude_list = []
      self.name = self.target
      if not name == "":
         self.name = name
      for ex in excludes:
         self.exclude_list.append("--exclude="+ ex)
      self.bparse = backup_parser('{0}/{1}.backup'.format(self.dest, self.name))
      print self.bparse.backups

   def partial(self):
      outfile = self.run("part", max(self.bparse.backups.keys()))
      self.bparse.add_backup(outfile)

   def full(self):
      outfile = self.run("full", curdate)
      with open(self.dest+"/"+self.name+".backup", "a") as bf:
         bf.write(curdate + " {\n" + outfile + "\n}\n")

   def run(self, backtype, backupdate):
      oldp = os.getcwd()
      if not self.target_dir == "":
         os.chdir(self.target_dir)
      outname = "{0}/{1}-{2}-{3}.tbz".format(self.dest, self.name, backtype, curdate)
      snarname = "{0}/{1}-{2}.snar".format(self.dest, self.name, backupdate)
      listfile = "{0}/{1}-{2}.tarlist".format(self.dest, self.name, backupdate)
      args=['tar', '-cjvf', outname, '--one-file-system','-g', snarname]
      args.extend(self.exclude_list)
      args.append(self.target)
      #print str(args)
      call(args)
      #with open(listfile, 'a') as f:
      #   f.write(os.path.basename(outname) + "\n")
      os.chdir(oldp)
      return os.path.basename(outname)

snar_date=curdate
from config import *

if (len(sys.argv) < 2):
   print 'backup.py source destination [config]'
   sys.exit(1)

backup_type = sys.argv[1]

if len(sys.argv) > 2:
   backup_source = sys.argv[2]

if len(sys.argv) > 3:
   backup_dest = sys.argv[3]

back_ob = backup(backup_source, backup_dest, excludes=['.cache'])
if backup_type == "full":
   back_ob.full()
elif backup_type == "partial":
   back_ob.partial()
else:
   print 'backup.py source destination [config]'
   sys.exit(1)



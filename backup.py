#!/usr/bin/python

import sys
import os
import os.path
from subprocess import call
import datetime
from configparser import backup_parser, config_parser, arg_parser


now= datetime.datetime.now()
curdate = now.strftime("%Y-%m-%dT%H:%M:%S")

class backup:
   def __init__(self):
      pass
   #def __init__(self, path_to_target, destination, excludes=[], name=""):
   def __init__(self, options):
      self.target = os.path.basename(options['target'])
      self.dest = options['dest']
      self.target_dir = os.path.dirname(options['target'])
      self.exclude_list = []
      self.name = self.target
      if not options['name'] == "":
         self.name = options['name']
      for ex in options['exclude']:
         self.exclude_list.append("--exclude="+ ex)
      self.bparse = backup_parser('{0}/{1}.backup'.format(self.dest, self.name))

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


if (len(sys.argv) < 2):
   print 'backup.py source destination [config]'
   sys.exit(1)

backup_type = sys.argv[1]

cparse = config_parser(os.environ["HOME"] + "/.pytarbak")
options = cparse.get_options()
aparse = arg_parser(sys.argv[2:], opt=options)

p = aparse.options['profile']
if p != "default":
   aparse = arg_parser(sys.argv[2:], opt=cparse.get_options(profile=p))

options = aparse.options

#back_ob = backup(backup_source, backup_dest, excludes=['.cache'])
back_ob = backup(options)
if backup_type == "full":
   back_ob.full()
elif backup_type == "partial":
   back_ob.partial()
else:
   print 'backup.py source destination [config]'
   sys.exit(1)



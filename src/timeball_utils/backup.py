#!/usr/bin/python
#      backup.py : handles the creation of the backups
#      Copyright (C) 2013  Kevin Brandstatter <icarusthecow@gmail.com>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.


import sys
import os
import os.path
from subprocess import check_call, CalledProcessError
import datetime
from configparser import backup_parser, config_parser, arg_parser, usage
from shutil import copyfile, move


now= datetime.datetime.now()
curdate = now.strftime("%Y-%m-%dT%H:%M:%S")

class backup:
   def __init__(self):
      pass
   #def __init__(self, path_to_target, destination, excludes=[], name=""):
   def __init__(self, options):
      self.target = os.path.basename(options['target'])
      self.dest = os.path.realpath(options['dest'])
      self.target_dir = os.path.dirname(options['target'])
      self.exclude_list = []
      if options['name'] == "":
         options['name'] = self.target
      self.name = self.target
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
      # We'll just tar it first to avoid complications with child processes like bzip2
      outname = "{0}/{1}-{2}-{3}.tar".format(self.dest, self.name, backtype, curdate)
      snarname = "{0}/{1}-{2}.snar".format(self.dest, self.name, backupdate)
      #listfile = "{0}/{1}-{2}.tarlist".format(self.dest, self.name, backupdate)
      # Set the tar command line options
      args=['tar', '-cvf', outname, '--one-file-system','-g', snarname]
      args.extend(self.exclude_list)
      level = 0
      if backtype == "part":
         level=len(self.bparse.backups[backupdate])
      args.append("--level="+str(level))
      args.append(self.target)
      # Cleanup past backups that failed to complete
      self.cleanup_failed(snarname)
      if backtype == "part":
         copyfile(snarname, snarname+".bak")
      try:
         check_call(args)
      except CalledProcessError as e:
         logging.error("Backup failed with error code: " + str(e.returncode))
         if (e.returncode > 1): # Ignore errors from tar
            os.remove(outname)
            if backtype == "part":
               move(snarname+".bak", snarname)
            sys.exit(e.returncode)
         logging.warning("Files that were modified or changed during the backup may be corrupted")
      try:
         logging.info("Archive finished, compressing with bzip2")
         check_call(['bzip2', outname])
         outname = outname + '.bz2'
         logging.info("Compression complete")
      except CalledProcessError as e:
         logging.error("Compression failed")
      #with open(listfile, 'a') as f:
      #   f.write(os.path.basename(outname) + "\n")
      if backtype == "part":
         os.remove(snarname+".bak")
      os.chdir(oldp)
      return os.path.basename(outname)

   def cleanup_failed(self, snarname):
      # If backup failed, restore snar from backup
      if os.path.exists(snarname + ".bak"):
         logging.info("Snar backup file found, recovering")
         move(snarname+".bak", snarname)
         # TODO remove the unecessary archives

def run(args):
   if (len(args) < 2):
      print usage
      sys.exit(1)

   backup_type = args[1]

   cparse = config_parser(os.environ["HOME"] + "/.timeball")
   options = cparse.get_options()
   aparse = arg_parser(args[2:], opt=options)

   p = aparse.options['profile']
   if p != "default":
      aparse = arg_parser(args[2:], opt=cparse.get_options(profile=p))

   options = aparse.options

   if options['target'] == "":
      print "No target specified"
      print usage
      sys.exit(1)
   if options['dest'] == "":
      print "No destination specified"
      print usage
      sys.exit(1)

   #back_ob = backup(backup_source, backup_dest, excludes=['.cache'])
   back_ob = backup(options)
   if backup_type == "full":
      back_ob.full()
   elif backup_type == "partial":
      back_ob.partial()
   else:
      print usage
      sys.exit(1)

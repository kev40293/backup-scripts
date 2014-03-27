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
from configparser import backup_parser, config_parser
from shutil import copyfile, move
import logging



class backup:
   def __init__(self, options):
      self.target = os.path.basename(options['target'])
      self.dest = os.path.realpath(options['dest'])
      self.target_dir = os.path.dirname(options['target'])
      if not options['name']:
         options['name'] = self.target
      self.name = self.target
      self.exclude_args = self.get_exclude_args(options['exclude'])
      self.backup_type = options['back_type']
      self.init_filenames()

   def init_filenames(self):
      self.bparse = backup_parser('{0}/{1}.backup'.format(self.dest, self.name))
      self.date = self.get_backup_date()
      self.tar_name = "{0}/{1}-{2}-{3}.tar".format(self.dest, self.name, self.backup_type, self.date)
      self.snar_name = "{0}/{1}-{2}.snar".format(self.dest, self.name, self.date)

   def get_exclude_args(self, exclude_options):
      excluded_files = []
      for ex in exclude_options:
         excluded_files.append("--exclude="+ ex)
      return excluded_files

   def get_backup_date(self):
      if self.backup_type == "part":
         if (len(self.bparse.backups.keys()) == 0):
            logging.error("No full backup to base a partial off of")
            exit(1)
         else:
            return max(self.bparse.backups.keys())
      else:
         now= datetime.datetime.now()
         return now.strftime("%Y-%m-%dT%H:%M:%S")

   def do_backup(self):
      self.setup_backup()
      self.create_tar()
      self.compress_archive()
      self.record_backup()
      os.chdir(self.original_directory)

   def setup_backup(self):
      self.push_directory()
      self.remove_unfinished_backups()
      if self.backup_type == "part":
         logging.info("Backing up snar file")
         copyfile(self.snar_name, self.snar_name+".bak")

   def push_directory(self):
      self.original_directory = os.getcwd()
      if not self.target_dir == "":
         os.chdir(self.target_dir)

   def remove_unfinished_backups(self):
      if os.path.exists(self.snar_name + ".bak"):
         logging.info("Snar backup file found, recovering")
         move(self.snar_name+".bak", self.snar_name)
         # TODO remove the unecessary archives

   def record_backup(self):
      if self.backup_type == "full":
         self.bparse.add_backup(self.tar_name+".bz2", date=self.date)
      elif self.backup_type == "part":
         self.bparse.add_backup(self.tar_name+".bz2")
         os.remove(self.snar_name+".bak")

   def create_tar(self):
      args = self.get_tar_options()
      try:
         check_call(args)
      except CalledProcessError as e:
         logging.error("Backup failed with error code: " + str(e.returncode))
         if (e.returncode > 2): # Ignore errors from tar
            self.cleanup_failed_archive()
            sys.exit(e.returncode)
         logging.warning("Files that were modified or changed during the backup may be corrupted")

   def cleanup_failed_archive(self):
      os.remove(self.tar_name)
      if self.backup_type == "part":
         move(self.snar_name+".bak", self.snar_name)
      if self.backup_type == "full":
         os.remove(self.snar_filename)

   def get_tar_options(self):
      args=['tar', '-cvf', self.tar_name, '--one-file-system','-g', self.snar_name]
      args.extend(self.exclude_args)
      args.append(self.target)
      return args

   def compress_archive(self):
      try:
         logging.info("Archive finished, compressing with bzip2")
         check_call(['bzip2', self.tar_name])
         logging.info("Compression complete")
      except CalledProcessError as e:
         logging.error("Compression failed")


def run(options):
   back_ob = backup(options)
   back_ob.do_backup()

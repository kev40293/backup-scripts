#!/usr/bin/python
#      configparser.py : handles the parsing of arguments and the config file
#      Copyright (C) 2013  Kevin Brandstatter <icarusthecow@gmail.com>
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.

import re, os, sys
import logging

def default_opts():
   return{
      "name": None,
      "target": None,
      "dest": None,
      "exclude": [],
      "profile": "default",
      "log-level": "warning",
      "back_type": None
      }

class parser:
   def __init__(self, filename):
      self.stream = ""
      try:
         with open(filename) as inf:
            self.stream += inf.read()
      except:
         pass

   def spaces(self):
      #m = re.match('\Ai(\s*)', self.stream)
      self.stream = self.stream.lstrip()

      pass

   def parseLine(self):
      m = re.match('\A([^\n{}]*)', self.stream)
      if m.group(0) == "":
         return None
      self.stream = self.stream.lstrip(m.group(0))
      self.spaces()
      return m.group(0)

   def parseString(self):
      m = re.match('\A([^ \t\n\r\f\v={}]*)', self.stream)
      if m.group(0) == "":
         return None
      self.stream = self.stream.lstrip(m.group(0))
      self.spaces()
      return m.group(0)

   def symbols(self, sym):
      m = re.match('\A('+sym+')', self.stream)
      if m == None:
         return None
      self.stream = self.stream.lstrip(m.group(0))
      self.spaces()
      return m.group(0)

   def parseBlock(self):
      curstream = self.stream
      s = self.symbols("{")
      if s ==  None:
         self.stream = curstream
         return None
      exp_list = []
      expr = ""
      # parse a single line of the block
      while self.symbols("}") is None:
         curstream = self.stream
         expr = self.parseLine()
         if expr is None:
            self.stream = curstream
            return None
         exp_list.append(expr)
      self.spaces()
      return exp_list

   def parseConfBlock(self):
      curstream = self.stream
      header = self.parseString()
      expr_list = self.parseBlock()
      if header is None or expr_list is None:
         self.stream = curstream
         return (None, None)
      return (header, expr_list)

   def empty(self):
      return self.stream == ""

class backup_parser(parser):
   backups = dict()
   def __init__(self, backup_file):
      parser.__init__(self, backup_file)
      self.filename = backup_file
      self.read_backup_file()

   def read_backup_file(self):
      while True:
         date = self.parseString()
         if date is None:
            break
         backup_list = self.parseBlock()
         self.backups[date] = backup_list
      return self.backups

   def add_backup(self, outfile, date=None):
      outfile = os.path.basename(outfile)
      if date is None:
         date = max(self.backups.keys())
      if date not in self.backups.keys():
         self.backups[date] = [outfile]
      else:
         self.backups[date].append(outfile)
      self.write_backup()

   def remove_backup(self, key):
      self.backups.pop(key, None)
      self.write_backup()

   def write_backup(self):
      try:
         with open(self.filename, "w") as cf:
            for key in self.backups.keys():
               cf.write(key + " {\n")
               for v in self.backups[key]:
                  cf.write(v + "\n")
               cf.write("}\n")
      except IOError:
          logging.error("Could not write to backup file")

class config_parser(parser):
   options_db = {
         "default": default_opts()
         }
   def __init__(self, config_file):
      parser.__init__(self, config_file)
      self.filename = config_file
      self.read_config()

   def read_config(self):
      if not os.path.exists(self.filename):
         with open(self.filename, 'w') as nf:
            print("Backup not found, creating new one")
            nf.write('default {\n}')
      with open(self.filename) as cf:
         profile, expL = self.parseConfBlock()
         while profile is not None:
            self.options_db[profile] = default_opts()
            for pair in expL:
               arg, val = pair.split("=")
               arg = arg.rstrip()
               val = val.lstrip()
               if arg == "exclude":
                     self.options_db[profile][arg].append(val)
               else:
                  self.options_db[profile][arg] = val
            profile, expL = self.parseConfBlock()
      return self.options_db

   def get_options(self, profile="default"):
      return self.options_db[profile]
   def get_opt(self, option, profile="default"):
      try:
         return self.options_db[profile][option]
      except KeyError:
         return None

class arg_parser(parser):
   def __init__(self, args, opt=None):
      self.stream = "\n".join(args)
      self.options = opt
      self.raw = list()
      if self.options is None:
         self.options = default_opts()
      self.parse_args()
   def parse_args(self):
      while True:
         arg, val = self.parseArg()
         if val is None:
            if arg == "help":
               print(usage)
               sys.exit(1)
            break
         elif arg is None:
            self.raw.append(val)
         elif arg == "exclude":
            self.options[arg].append(val)
         else:
            self.options[arg] = val
      if len(self.raw) > 0:
         self.options['target'] = self.raw[0]
      if len(self.raw) > 1:
         self.options['dest'] = self.raw[1]

   def parseArg(self):
      curstream = self.stream
      if self.symbols("--") is None:
         argex = self.parseLine()
         return None, argex
      argex = self.parseLine()
      try:
         k, v = argex.split("=")
      except ValueError:
         return argex, None
      return k.rstrip(), v.lstrip()

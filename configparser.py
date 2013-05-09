#!/usr/bin/python
import re, os

def default_opts():
   return{
      "name": "",
      "target": "",
      "dest": "",
      "exclude": [],
      "profile": "default"
      }

class parser:
   def __init__(self, filename):
      self.stream = ""
      try:
         with open(filename) as inf:
            self.stream += inf.read()
      except:
         return None

   def spaces(self):
      #m = re.match('\Ai(\s*)', self.stream)
      self.stream = self.stream.lstrip()

      pass

   def parseString(self):
      m = re.match('\A([^ \t\n\r\f\v={}]*)', self.stream)
      self.stream = self.stream.lstrip(m.group(0))
      self.spaces()
      if m.group(0) == "":
         return None
      return m.group(0)

   def symbols(self, sym):
      m = re.match('\A('+sym+')', self.stream)
      if m == None:
         return None
      self.stream = self.stream.lstrip(m.group(0))
      self.spaces()
      return m.group(0)

   def parseBlock(self):
      s = self.symbols("{")
      if s ==  None:
         return None
      exp_list = []
      while self.symbols("}") is None:
         st = self.parseString()
         if self.symbols("=") is not None:
            st += "=" + self.parseString()
         exp_list.append(st)
      self.spaces()
      return exp_list

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

   def add_backup(self, outfile):
      snardate = max(self.backups.keys())
      self.backups[snardate].append(outfile)
      with open(self.filename, "w") as cf:
         for key in self.backups.keys():
            cf.write(key + " {\n")
            for v in self.backups[key]:
               cf.write(v + "\n")
            cf.write("}\n")

class config_parser(parser):
   options_db = {
         "default": default_opts()
         }
   def __init__(self, config_file):
      parser.__init__(self, config_file)
      self.filename = config_file
      self.read_config()

   def read_config(self):
      with open(self.filename) as cf:
         while True:
            profile = self.parseString()
            if profile is None:
               break
            self.options_db[profile] = default_opts()
            confs = self.parseBlock()
            for pair in confs:
               arg, val = pair.split("=")
               if arg == "exclude":
                     self.options_db[profile][arg].append(val)
               else:
                  self.options_db[profile][arg] = val
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
      self.stream = " ".join(args)
      self.options = opt
      if self.options is None:
         self.options = default_opts()
      self.parse_args()
   def parse_arg(self):
      if self.symbols("--") is None:
         return False
      k = self.parseString()
      if self.symbols("=") is None:
         return False
      v = self.parseString()
      if k == "exclude":
         self.options[k].append(v)
      else:
         self.options[k] = v
      return True

   def parse_args(self):
      while self.parse_arg():
         pass
      src = self.parseString()
      dest = self.parseString()
      if src is not None:
         self.options['target'] = os.path.realpath(src)
      if dest is not None:
         self.options['dest'] = os.path.realpath(dest)


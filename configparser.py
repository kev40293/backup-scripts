#!/usr/bin/python
import re


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
      m = re.match('\A([\S:]*)', self.stream)
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


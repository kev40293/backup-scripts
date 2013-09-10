import unittest
from sys import path
path.insert(0,'../src/')

import os

from timeball_utils.backup import backup;
from timeball_utils.configparser import default_opts

class TestBackupFunctions (unittest.TestCase):

   base_options = {
         "name": "test",
         "target" : "test",
         "dest": ".",
         "exclude": [],
         "profile": "default",
         "log-level": "warning",
         "back_type": "full"
         }

   def setUp(self):
      self.backup_test = backup(self.base_options)

   def test_initialized(self):
      self.assertTrue(self.backup_test is not None)
      self.assertTrue(self.backup_test.name == "test")
      self.assertTrue(self.backup_test.target == "test")
      self.assertTrue(self.backup_test.dest == os.path.realpath("."))
      self.assertTrue(self.backup_test.exclude_args == [])

   def test_get_exclude_list(self):
      excludes = ['one', 'two', 'three and a half']
      exclude_args = self.backup_test.get_exclude_args(excludes)
      self.assertTrue('--exclude=one' in exclude_args)
      self.assertTrue('--exclude=two' in exclude_args)
      self.assertTrue('--exclude=three and a half' in exclude_args)

   def test_partial_backup(self):
      self.assertTrue(False)

   def test_full_backup(self):
      self.assertTrue(False)

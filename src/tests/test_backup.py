import unittest
from sys import path

import os
import datetime

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

   example_backups = {
         "2013-07-18T23:11:30" : [
            "kevin-full-2013-07-18T23:11:30.tar.bz2",
            "kevin-part-2013-07-19T16:32:49.tar.bz2",
            "kevin-part-2013-07-21T12:43:23.tar.bz2",
            "kevin-part-2013-07-22T19:41:57.tar.bz2",
            "kevin-part-2013-07-23T16:04:46.tar.bz2",
            "kevin-part-2013-07-24T17:46:00.tar.bz2",
            "kevin-part-2013-07-25T16:42:30.tar.bz2",
            "kevin-part-2013-07-27T12:23:09.tar.bz2",
            "kevin-part-2013-07-28T16:30:13.tar.bz2",
            "kevin-part-2013-07-29T16:57:56.tar.bz2",
            "kevin-part-2013-07-30T16:26:35.tar.bz2"
            ]
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

   def test_remove_unfinished_backups(self):
      self.backup_test.remove_unfinished_backups()
      with open(self.backup_test.snar_name+".bak", "w"):
         pass
      self.backup_test.remove_unfinished_backups()
      os.remove(self.backup_test.snar_name)

   def test_get_full_backup_date(self):
      self.assertEquals(self.backup_test.get_backup_date(), datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

   def test_get_partial_backup_date(self):
      self.backup_test.bparse.backups = self.example_backups
      self.backup_test.backup_type = "part"
      self.assertEquals(self.backup_test.get_backup_date(), "2013-07-18T23:11:30")

import unittest
from sys import path, argv

from timeball_utils.argparser import *

class TestBackupArgumentParser(unittest.TestCase):
    def setUp(self):
        self.def_cl = ['backup', 'target', 'dest']
    def testNofunction(self):
        with self.assertRaises(SystemExit):
            options = parse_cl([], default_opts)

    def testBacktype(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['back_type'], 'backup')
    def testParsedBasic(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['target'], 'target')
        self.assertEquals(options['dest'], 'dest')

class TestRecoveryArgumentParser (unittest.TestCase):
    def setUp(self):
        self.def_cl = ['recover', 'target-file', 'dest']
    def testBacktype(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['back_type'], 'recover')
    def testParsed(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['backup-file'], 'target-file')
        self.assertEquals(options['dest'], 'dest')

class TestDeleteArgumentParser (unittest.TestCase):
    def setUp(self):
        self.def_cl = ['delete', 'target-file']
    def testBacktype(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['back_type'], 'delete')
    def testParsed(self):
        options = parse_cl(self.def_cl, default_opts)
        self.assertEquals(options['backup-file'], 'target-file')

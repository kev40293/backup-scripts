import unittest
import mock
from timeball_utils.configparser import parser

class TestParser(unittest.TestCase):
   def setUp(self):
      self.pars = parser(None)

   def testSpaces(self):
      self.pars.stream="      something"
      self.pars.spaces()
      self.assertEquals(self.pars.stream, "something")

   def testSymbol(self):
      self.pars.stream= "meow more"
      first = self.pars.symbols("meow")
      self.assertEquals(first, "meow")
      first = self.pars.symbols("mo")
      self.assertEquals(first, "mo")
      first = self.pars.symbols("mo")
      self.assertEquals(first, None)
      self.assertEquals(self.pars.stream, "re")


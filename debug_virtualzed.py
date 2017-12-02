#!/usr/bin/python
import unittest
import os
import serial

import random
import time
import string

import lib.virtual_terminal as vt

class virtual_terminal_feature_check(unittest.TestCase):
   

    def randstring(self):
        workingstring = str()
        for unused in range(0,random.randint(0,self.max_length)):
           workingstring += random.choice(self.char_opts)
        return workingstring

    @classmethod
    def setUp(self):


    def test_creation(self):

    def test_master_to_slave_comms(self):


if __name__ == '__main__':
    unittest.main()


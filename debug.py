#!/usr/bin/python
import unittest
import os
import serial

import random
import time
import string

import lib.virtual_terminal as vt

class virtual_terminal_feature_check(unittest.TestCase):
   

    def randstring(length,opts):
        workingstring = ""
        for unused in range(0,random.randint(0,length)):
           workingstring += random.choice(opts)

    def setUp(self):
        virSerial = vt.virtualserialport()
        masterInterface = serial.Serial(virSerial.master_descriptor)
        repetitions = 500
        max_length  = 256
        char_opts   = string.printable
        random.seed(time.time())

    def test_creation(self):
        self.assertTrue(type(virSerial.slave_descriptor), type(os.__file__))
        self.assertTrue(type(virSerial.master_descriptor), type(os.__file__))

    def test_slave_to_master_comms(self):
        for unused in range(0,repetitions):
            teststring = randstring()
            virSerial.send(teststring)
            self.assertEqual(virSerial.interface.out_waiting,0)
            self.assertEqual(masterInterface.in_waiting, len(teststring))
            self.assertEqual(masterInterface.read_all(), teststring)

    #def test_master_to_slave_comms(self):

if __name__ == '__main__':
    unittest.main()


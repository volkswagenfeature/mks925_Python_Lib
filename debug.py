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
        self.virSerial = vt.virtualserialport()
        self.masterInterface = serial.Serial(self.virSerial.master_descriptor)
        self.repetitions = 2 
        self.max_length  = 256
        self.char_opts   = string.printable
        random.seed(time.time())

    def test_creation(self):
        self.assertIsInstance(self.virSerial.slave_descriptor, type(os.__file__))
        self.assertIsInstance(self.virSerial.master_descriptor, type(os.__file__))

    def test_slave_to_master_comms(self):
        for test_num in range(0,self.repetitions):
            teststring = self.randstring()
            with self.subTest(tst_n=test_num ):
                self.virSerial.send("teststring")
                self.assertEqual(self.virSerial.interface.out_waiting,0
                self.assertEqual(self.masterInterface.in_waiting, len("teststring"))
                self.assertEqual(self.masterInterface.read_all(), "teststring")


    #def test_master_to_slave_comms(self):

if __name__ == '__main__':
    unittest.main()


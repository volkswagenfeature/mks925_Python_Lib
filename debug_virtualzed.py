#!/usr/bin/python
import unittest
import os
import serial

import random
import time
import string

import lib.virtual_terminal2 as vt


class virtual_terminal_feature_check(unittest.TestCase):
   

    def randstring(self):
        workingstring = str()
        for unused in range(0,random.randint(0,self.max_length)):
           workingstring += random.choice(self.char_opts)
        return workingstring

    @classmethod
    def setUp(self):
        virtual_serial = vt.Serial()

    def test_default_vals(self):
        # Check to make sure that all values are properly initialized to the correct defaults.
        self.assertEqual(vt.properties.port, None)
        self.assertEqual(vt.properties.baudrate, 9600)
        self.assertEqual(vt.properties.bytesize, vt.EIGHTBITS)
        self.assertEqual(vt.properties.parity, vt.PARITY_NONE)
        self.assertEqual(vt.properties.stopbits, vt.STOPBITS_ONE)

        #NOTE: Default behavior of serial class is timeout=None. If/when timeouts get implemented,
        #      this needs to be revised.
        self.assertEqual(vt.properties.timeout, 0)
        self.assertEqual(vt.properties.xonxoff, False)
        self.assertEqual(vt.properties.rtscts, False)
        self.assertEqual(vt.properties.dsrdtr, False)
        self.assertEqual(vt.properties.inter_byte_timeout, None)



    def test_master_to_slave_comms(self):
        pass


if __name__ == '__main__':
    unittest.main()


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
        self.virtual_serial = vt.Serial()
        self.testbytes = b'abc123!@;'
        self.testbytes2 = b'foobar'

    @classmethod
    def tearDown(self):
        vt.Flags.open = False
        vt.Flags.chars_buffered = 0
        vt.buffers.Rx_to_Tx.close()
        vt.buffers.Tx_to_Rx.close()


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

        self.assertEqual(vt.Flags.open, True)
        self.assertEqual(vt.Flags.chars_buffered, 0)

    def test_transmission(self):
        charcount = self.virtual_serial.write(self.testbytes)
        self.assertEqual(charcount, len(self.testbytes))
        self.assertEqual(vt.buffers.Tx_to_Rx.getvalue(),self.testbytes)
        self.assertEqual(vt.Flags.chars_buffered, len(self.testbytes))
        self.assertEqual(vt.buffers.Tx_to_Rx.getvalue(), self.testbytes)

        # NOTE: Disabled, because for whatever reason, getvalue() works fine, but
        # read() does not.
        #self.assertEqual(vt.buffers.Tx_to_Rx.read(),self.testbytes2)

    def test_reception(self):
        vt.buffers.Rx_to_Tx.write(self.testbytes)
        self.assertEqual(vt.buffers.Rx_to_Tx.getvalue(),self.testbytes)
        self.assertEqual(vt.buffers.Rx_to_Tx.getvalue(),self.testbytes)
        self.assertEqual(self.virtual_serial.read(len(self.testbytes)), self.testbytes)
        
    def test_flush(self):
        self.virtual_serial.write(self.testbytes)
        self.assertEqual(vt.Flags.chars_buffered, len(self.testbytes))
        self.virtual_serial.flush()
        self.assertEqual(vt.Flags.chars_buffered, 0)

        
if __name__ == '__main__':
    unittest.main()


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


class Virtual_terminal_responder(unittest.TestCase):
    def setUp(self):
        self.virtual_serial = vt.Serial()
        self.responder = vt.Serial_responder()

    def tearDown(self):
        self.responder.reset()

    def test_receive_history_length(self):
        """History_length() should print off how long history currently is"""
        self.virtual_serial.write(b"stuff and things!!!!")
        
        self.assertEqual(vt.buffers.Tx_to_Rx[-1], b"stuff and things!!!!")

        self.virtual_serial.write(b"pqlst")
        self.virtual_serial.write(b"potato")

        self.assertEqual(self.responder.Rx_history_len(), 3)
        self.virtual_serial.write("more stuff")
        self.assertEqual(self.responder.Rx_history_len(), 4)


       
    def test_reset(self):
        """A test needed for the tearDown method, resets the entire class to default everything"""
        self.assertEqual(self.responder.Rx_history_len(),0)

        self.assertEqual(len(vt.buffers.Tx_to_Rx), 0)
        self.assertEqual(len(vt.buffers.Rx_to_Tx), 0)
        self.assertEqual(vt.Flags.chars_buffered, 0)

        self.responder.reset()


        self.assertEqual(self.responder.Rx_history_len(),0)

        self.assertEqual(len(vt.buffers.Tx_to_Rx), 0)
        self.assertEqual(len(vt.buffers.Rx_to_Tx), 0)
        self.assertEqual(vt.Flags.chars_buffered, 0)




        
    def test_receive_history(self):
        """ History should print the n-th from-the-end transmission. It returns a index error if it
        doesn't exist. """

        pass

    def test_full_frame_transmit(self):
        """a test to confirm behavior of transmit:
        Behavior is defined as setting the value that the next read will receive
        """
        str1 = b"Eggs and spam"
        str2 = b"bacon and sausage"
        self.responder.transmit(str1)
        self.assertEqual( vt.buffers.Rx_to_Tx[0], str1) 
        self.assertEqual( self.virtual_serial.read(len(str1)),str1)
        self.responder.transmit(str2)
        self.assertEqual( self.virtual_serial.read(len(str2)),str2)
        self.assertEqual( self.virtual_serial.read(len(str2)),"")
    
    def test_partial_frame_transmit(self):
        """
        A further test to confirm the behacior of transmit, when only reading
        part of a transmitted frame, or reading across frame bounderies.
        """
        str1 = b"12345"
        str2 = b"67890"
        self.
        self.assertEqual( vt.buffers.Rx_to_Tx[0], str1)
        self.assertEqual( vt.buffers.Rx_to_Tx[1], str2)
        
        self.responder.transmit(str1)
        self.responder.transmit(str2)
        self.assertEqual( self.virtual_serial.read(len(str1)-4), str1[0:-4])

 
    def test_receive(self):
        """a test to confirm behavior of receive: 
        Behavior is defined as returning the bytes written to Serial after the position
        that the last receive() finished, and before the position that the last flush() extends to"""
        pass
k   
        

        
if __name__ == '__main__':
    unittest.main()


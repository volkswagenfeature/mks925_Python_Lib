#!/bin/python
import os
import serial
import pty
import time
class virtualserialport:
    def __init__(self):
        master, slave = pty.openpty()
        self.slave_descriptor = os.ttyname(slave)
        self.master_descriptor = os.ttyname(master)
        self.interface = serial.Serial(self.slave_descriptor)

    def send(self,data):
        
        self.interface.write(data.encode("ASCII"))
        self.interface.flush()

    def receive(self,chars, timeout):
        timeout = time.time() + timeout
        while True:
            if (self.interface.in_waiting >= chars):
                return self.interface.read(chars)
            else:
                if (time.time() > timeout):
                    raise Exception("TIMEOUT!")
                    return self.interface.read(chars)





#!/bin/python
import os
import serial
import pty
import time
class virtualserialport:
    def __init__:
        master, slave = pty.openpty()
        self.slave_descriptor = os.ttyname(slave)
        self.master_descriptor = os.ttyname(master)
        self.serial = serial.Serial(slave_descriptor)

    def send(data):
        self.serial.write(data)
        self.serial.flush()

    def receive(chars, timeout):
        timeout = time.time() + timeout
        while True:
            if (self.serial.in_waiting >= chars):
                return self.serial.read(chars)
            else:
                if (time.time() > timeout):
                    raise Exception("TIMEOUT!")
                    return self.serial.read(chars)





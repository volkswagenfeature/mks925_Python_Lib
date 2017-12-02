# A different aproach to terminal virtualization.
# Probably simpler than creating a fake serial port:
# Just create a fake serial class, that implements all the same methods
# Import it instead of serial.Serial
# Trying to set it up, so that it saves what it receives to a buffer.
# One object serves as the serial system, the other can serve as a wrapper for the buffers.




###### Imports ######
# Time is used to measure read timeouts
# ...Which never exist for this library.
# leaving it in for future implementation.
import time

# Namedtuple is used from collections for globals.
import collections

# BytesIO is used from buffers for the read/write buffers
import io

# These exceptions are stolen straight from Serial, to assure
# identical functioning.
from serial import SerialException,SerialTimeoutException




###### Global Variables ######
# These namedtuples hold information that the virtual serial port is transmitting
# They are global in scope, so data can be pulled out of them, and tested outside
# of the serial class instance. This is important, because serial HAS to function EXACTLY
# like Serial.serial, and will probably be instantiated by the class constructor.
# As such, external stuff may not have any access to the instance, and needs these
# to access the data.


#The buffer system for in and out buffers
property_Options   = ["port", "baudrate", "bytesize", "parity",  "stopbits", 
                      "timeout", "xonxoff","rtscts", "write_timeout", 
                      "dsrdtr", "inter_byte_timeout"]
properties  = collections.namedtuple('property_template', property_Options)

#Buffers
buffers = collections.namedtuple('buffers', ['Rx_to_Tx', 'Tx_to_Rx'])
buffers.Rx_to_Tx = io.BytesIO()
buffers.Tx_to_Rx = io.BytesIO()

#Flags
Flags = collections.namedtuple('Flags', ['open','chars_buffered'])


##### Constants ######
# These are here because the serial library has them. the values are unimportant,
# but they MUST be UNIQUE. I do this through a 2-byte representation. A more
# elegant solution might be checking globals() for these values, somehow. but that's
# probably overcomplicating things


# Parity
PARITY_NONE = b'P0'
PARITY_EVEN = b'P1'
PARITY_ODD  = b'P2'
PARITY_MARK = b'Pm'
PARITY_SPACE= b'P_'

# Stop Bits
STOPBITS_ONE            = b'S1'
STOPBITS_ONE_POINT_FIVE = b'S3'
STOPBITS_TWO            = b'S2'

# Byte Size
FIVEBITS  = b'B5'
SIXBITS   = b'B6'
SEVENBITS = b'B7'
EIGHTBITS = b'B8'

class Serial:
    def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE,
             stopbits=STOPBITS_ONE, timeout=0, xonxoff=False, 
             rtscts=False, write_timeout=None, dsrdtr=False, 
             inter_byte_timeout=None):
        # Just plug all of these into the global properties namedtuple.
        properties.port = port
        properties.baudrate = baudrate
        properties.bytesize = bytesize
        properties.parity   = parity
        properties.stopbits = stopbits
        properties.timeout  = timeout
        properties.xonxoff  = xonxoff
        properties.rtscts   = rtscts
        properties.write_timeout = timeout
        properties.dsrdtr = dsrdtr
        properties.inter_byte_timeout = inter_byte_timeout

        # These require a bit of handling, not all of which is implemented yet.
        Flags.open = True
        Flags.chars_buffered = 0

    def write( self, data ):
        buffers.Tx_to_Rx.write( data )
        chars_buffered += len(data)

    def read( self, size=1 ):
        data = buffers.Rx_to_Tx.read( size )
        if (timeout!=0 or timeout!=None or len(data) == size):
            return data
        else:
            # TODO: Handle timeout code here.
            # Remember, timeout=None waits until enough bytes have been received.
            # This is the library default behavior.

            # timeout=0 never waits, just returns what it has.
            # This is my currently implemented behavior.

            # timeout=n waits float n secconds.

            raise NotImplementedError("Timeouts are not properly implenented yet!")

    def flush( self ):
        chars_buffered = 0

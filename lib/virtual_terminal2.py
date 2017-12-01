# A different aproach to terminal virtualization.
# Probably simpler than creating a fake serial port:
# Just create a fake serial class, that implements all the same methods
# Import it instead of serial.Serial
# Trying to set it up, so that it saves what it receives to a buffer.
# One object serves as the serial system, the other can serve as a wrapper for the buffers.

# Keeping the old version in, in case we just want to stick with that.
# BTW, I won't be able to make it Monday the 27th, I procreastinated on a bunch of stuff
# And have to study and other stuff.


import uuid
import collections
import io

#The buffer system for in and out buffers
property_Options   = ["port", "baudrate", "bytesize", "stopbits", 
                      "timeout", "xonxoff","rtscts", "write_timeout", 
                      "dsrdtr", "inter_byte_timeout"]
properties  = collections.namedtuple('property_template', Buffer_Properties)

#Buffers
buffers = collections.namedtuple('buffers', ['Rx_to_Tx', 'Tx_to_Rx'])
buffers.Rx_to_Tx = io.BytesIO()
buffers.Tx_to_Rx = io.BytesIO()

#Flags
Flags = collections.namedtuple('Flags', ['open','chars_buffered']


##### Constants ######
# Parity
PARITY_NONE = uuid.uuid4()
PARITY_EVEN = uuid.uuid4()
PARITY_ODD  = uuid.uuid4()
PARITY_MARK = uuid.uuid4()
PARITY_SPACE= uuid.uuid4()

# Stop Bits
STOPBITS_ONE            = uuid.uuid4()
STOPBITS_ONE_POINT_FIVE = uuid.uuid4()
STOPBITS_TWO            = uuid.uuid4()

# Byte Size
FIVEBITS  = uuid.uuid4()
SIXBITS   = uuid.uuid4()
SEVENBITS = uuid.uuid4()
EIGHTBITS = uuid.uuid4()

class Serial:
    def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, 
             stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, 
             rtscts=False, write_timeout=None, dsrdtr=False, 
             inter_byte_timeout=None):
        properties.port = port
        properties.baudrate = baudrate
        properties.bytesize = bytesize
        properties.stopbits = stopbits
        properties.timeout  = timeout
        properties.xonxoff  = xonxoff
        properties.rtscts   = rtscts
        properties.write_timeout = timeout
        properties.dsrdtr = dsrdtr
        properties.inter_byte_timeout = inter_byte_timeout
        
        Flags.open = True
        Flags.chars_buffered = 0

    def write( self, data ):
        buffers.Tx_to_Rx.write( data )
        chars_buffered += len(data)

    def read( self, size=1 ):
        buffers.Rx_to_Tx.read( size )

    def flush( self ):
        chars_buffered = 0



import serial

class MKS925:
    class __MKS_msg__:
        def __init__(self, msg_types, msg_format, response_format, docstring):
            self.msg_types       = msg_types
            self.msg_format      = msg_format
            self.response_format = response_format
            self.docstring       = docstring
    
    class __MKS_wrapper__:
        # TODO: These wrap a dict of MKS Messages, and 
        # TODO: modify their dot operator to properly send the command.
    def __init__(self,adr=253,baud=9600,port='/dev/ttyS0'):
        # Set up vars and create serial port
        self.baudrate = baud
        self.serialport = port
        self.address = adr
        self.serialport = serial.Serial(self.serialport, 
                                        self.baudrate)
        
        # Library of transmittable messages
        self.commands = {"Address":"AD",   "Baud":"BR",   "FactoryDefault":"FD",
                         "RSDelay":"RSD",  "Test":"TST",  "Unit":"U",
                         "Tag":"UT",       "Type":"DT",   "FirmwareV":"FV",
                         "HardwareV":"HV", "Origin":"MF", "Model":"MD",
                         "Pressure":"PR1", "Serial":"SN", "Uptime":"TIM"

                        
        self.queries
    def __send_generic__(self, msg_type, message, parameter=""):
        # Idiot checking for input parameters
        if (msg_type.find("!?") == -1 or msg_type.len() != 1):
            raise Exception("Invalid Message Type")

        # Format message to be sent
        commandtemplate = "@{0}{1}{2}{3};FF"
        formvals = [ self.address, message, msg_type, parameter]
        self.serialport.write(commandtemplate.format(formvals)
                                             .encode('ASCII'))

        # Read data from port
        rawin = self.serialport.read(3)
        if (rawin[0] != '@'):
            raise Exception("Invalid Packet Received")
        while (rawin[-3:-1] != ";FF"):
            rawin += self.serialport.read(1)

        # Process raw data
        if rawin.len() :
            if rawin.find("ACK"):
                res = rawin[1:-3].split("ACK")
                resaddress = res[0]
                resvalue = res[1]
                return resvalue
            elif rawin.find("NAK"):
                raise exception("NAK received!")
                return rawin[1:-3].split("NAK")[1]
            else:
                raise Exception( "Unexpected response!!")
                return ""
        else:
            raise Exception( "No Reply!!")
            return ""



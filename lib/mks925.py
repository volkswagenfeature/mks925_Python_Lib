# To interface with the serial port
import serial

# To format-check everything
import re

# TODO: Better exception handling. At the moment my exceptions are descriptive, but non-standard.
# TODO: Add more idiot checking for input parameters
# TODO: Broadcast support?? Multi-sensor support?? Not currently relevant, but might want.

class MKS925:
    def __send_generic(self, msg_type, message, parameter=""):
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
                raise Exception( "Unexpected response")
                return ""
        else:
            raise Exception( "No Reply")
            return ""


    class __MKS_msg:
        def __init__(self, msg_types, msg,  
                     response_format = None, 
                     parameter_format = response_format,
                     docstring = None):
            self.msg_types       = msg_types
            self.msg            = msg
            self.__doc__         = docstring
            self.calltype        = ""

            self.msg_format = "^"
            self.response_format = "^"
            if (parameter_format not None):
                self.msg_format      = re.compile(msg_format)
            if (response_format not None):
                self.response_format = re.compile(response_format)

        def __call__(self, parameter):
            if (self.calltype.len() > 0 and self.msg_types.find(self.calltype) != -1):
                if (self.parameter_format.match(parameter) != None):
                    result = __send_generic(self.calltype, self.msg, parameter)
                    # TODO: Need to be able to catch a NAK right here.
                    if (self.response_format.fullmatch(result) != None):
                        return result;
                    else:
                        raise Exception("Invalid response format")
                else:
                    raise Exception("Invailid Parameter Format")
            else:
                raise Exception("Invalid calltype passed")
            self.calltype = ""
    
    class __MKS_wrapper:
        # These wrap a dict of MKS Messages, and return them properly via the dot operator.
        def __init__(self, msg_type_handled, msg_dict):
            self.msg_dict = msg_dict
            self.msg_type_handled = msg_type_handled
        def __getattr__(self, key):
            msg_object = self.msg_dict[key]
            msg_object.calltype = self.msg_type_handled
            return msg_object
    
    def __init__(self,adr=253,baud=9600,port='/dev/ttyS0'):
        # Set up vars and create serial port
        self.baudrate = baud
        self.serialport = port
        self.address = adr
        self.serialport = serial.Serial(self.serialport, 
                                        self.baudrate)
        
        # Library of transmittable messages
        self.commands = dict()
        self.commands["baud"] = #TODO: Write out all message declaratons.

        # The three externaly accessable wrapper objects, for the "three" different things
        # you can do with MKS messages: Make Queries, Send commands, or Print docs.
        self.query      = __MKS_wrapper("TODO: Stuff in here")
        self.set        = __MKS_wrapper("TODO: Stuff in here")
        self.info_about = __MKS_wrapper("TODO: Stuff in here")

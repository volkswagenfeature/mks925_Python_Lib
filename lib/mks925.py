# To interface with the serial port
#import serial
import lib.virtual_terminal2 as serial

# To format-check everything
import re

# TODO: Better exception handling. At the moment my exceptions are descriptive, but non-standard.
# TODO: Add more idiot checking for input parameters
# TODO: Broadcast support?? Multi-sensor support?? Not currently relevant, but might want.
# TODO: Make sure sensor values are padded appropriately
# TODO: Make sure everything sends ASCII and not unicode
class NACKError(ConnectionError):
    def __init__(self,value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class MKS925:
    def __send_generic(self, msg_type, message, parameter=""):

        # Format message to be sent
        commandtemplate = "@{0}{1}{2}{3};FF"
        formvals = ( self.address, message, msg_type, parameter)
        self.serialport.write(commandtemplate.format(*formvals)
                                             .encode('ASCII'))
        

        # Flush data, and Read data from port
        self.serialport.flush()
        rawin = self.serialport.read()
        if ((len(rawin) == 0) or (rawin[0] != '@')):
            raise ConnectionError("Invalid Reply")
        while (rawin[-3:-1] != ";FF"):
            rawin += self.serialport.read(1)

        # Process raw data
        if rawin.find("ACK"):
            res = rawin[1:-3].split("ACK")
            resaddress = res[0]
            resvalue = res[1]
            return resvalue
        elif rawin.find("NAK"):
            raise NACKError("NAK received")
            return rawin[1:-3].split("NAK")[1]
        else:
            raise ConnectionError( "Invalid Reply")
        # Return raw data for debugging. 
        return rawin


    class __MKS_msg:
        def __init__(self, msg_types, msg,  
                     parameter_format = "^",
                     docstring = None):
            self.msg_types       = msg_types
            self.msg            = msg
            self.__doc__         = docstring
            self.calltype        = ""

            self.msg_format = re.compile(parameter_format)

        def __call__(self, parameter):
            if (self.calltype.len() > 0 and self.msg_types.find(self.calltype) != -1):
                if (self.parameter_format.match(parameter) != None):
                    result = __send_generic(self.calltype, self.msg, parameter)
                    # TODO: Need to be able to catch a NAK/malformed reply right here.
                else:
                    raise Exception("Invailid Parameter Format")
            else:
                raise Exception("Invalid calltype passed")
            self.calltype = ""
    
    class __MKS_wrapper:
        # These wrap a dict of MKS Messages, and return them properly via the dot operator.
        def __init__(self, msg_dict):
            self.msg_dict = msg_dict
        def __getattr__(self, key):
            msg_object = self.msg_dict[key]
            return msg_object

    #TODO: Object to format and produce consistent docstrings for thee __MKS_msg objects.
    #TODO: Right now, they're inconsistently formatted.
    
    def __init__(self,adr=253,baud=9600,port='/dev/ttyS0'):
        ################ Library of transmittable messages ###############
        self.commands = dict()


        # Interface commands
        self.commands['baudrate'] = self.__MKS_msg("!", "BR", "[0-9]{1,4}00", 
        "Changes the baudrate of the sensor. Sensor will reply with the baudrate that it will switch to at the old rate, before switching to the new one")

        self.commands['address'] = self.__MKS_msg("!?", "AD", "([0-1][0-9]{2})|(2[0-5]{2})",
        "Change sensor address to the value specified, or return the current address")

        # Setpoint Commands
        self.commands['point1_value'] = self.__MKS_msg("!", "SP1", "\d\.\d{3}E[+-]\d",
        "Change the pressure that the first setpoint relay activates")

        self.commands['point1_direction'] = self.__MKS_msg("!", "SD1", "(ABOVE)|(BELOW)",
        "Change if the first setpoint relay activates above or below the set pressure")

        self.commands['point1_hysterisis'] = self.__MKS_msg("!", "SH1", "\d\.\d{3}E[+-]\d",
        "Change the hysterisis of the first setpoint relay")

        self.commands['point1_enable'] = self.__MKS_msg("!","EN1", "(ON)|(OFF)",
        "Activates or Deactivates Setpoint 1")

        self.commands['point2_value'] = self.__MKS_msg("!", "SP2", "\d\.\d{3}E[+-]\d",
        "Change the pressure that the seccond setpoint relay activates")

        self.commands['point2_direction'] = self.__MKS_msg("!", "SD2", "(ABOVE)|(BELOW)",
        "Change if the second setpoint relay activates above or below the set pressure")

        self.commands['point2_hysterisis'] = self.__MKS_msg("!", "SH2", "\d\.\d{3}E[+-]\d",
        "Change the hysterisis of the second setpoint relay")

        self.commands['point2_enable'] = self.__MKS_msg("!","EN2", "(ON)|(OFF)",
        "Activates or Deactivates Setpoint 2")

        self.commands['point3_value'] = self.__MKS_msg("!", "SP3", "\d\.\d{3}E[+-]\d",
        "Change the pressure that the third setpoint relay activates")

        self.commands['point3_direction'] = self.__MKS_msg("!", "SD3", "(ABOVE)|(BELOW)",
        "Change if the third setpoint relay activates above or below the set pressure")

        self.commands['point3_hysterisis'] = self.__MKS_msg("!", "SH3", "\d\.\d{3}E[+-]\d",
        "Change the hysterisis of the third setpoint relay")

        self.commands['point3_enable'] = self.__MKS_msg("!","EN3", "(ON)|(OFF)",
        "Activates or Deactivates Setpoint 3")

        self.commands['safety_delay'] = self.__MKS_msg("!?", "SPD", "(ON)|(OFF)",
        "Safety delay is a feature that requires 5 successive reads to confirm the switching of a relay, to prevent false triggering due to noise. Command form sets it to a value, Query form requests its current value")

        #Commands for pressure reading and adjustment
        self.commands['pressure'] = self.__MKS_msg("?","PR1","",
        "Outputs the currently measured pressure")

        self.commands['gas_type'] = self.__MKS_msg("!?","GT","[A-Z0-9]{1-8}",
        "Query or change the type of gas that the sensor is calebrated to work properly in. Options include: Nitrogen, Argon, Helium, Hydrogen, Water, Neon, Carbon Dioxide and Xenon")

        self.commands['unit'] = self.__MKS_msg("!?", "U", "(TORR)|(MBAR)|(PASCAL)",
        "Query or change the unit of measurement used by the sensor")

        self.commands['zero_adjust']= self.__MKS_msg("!?", "VAC", "\d\.\d{3}E-[3-5]",
        "Change the low-level zero setpoint of the machine. Requires evacuation to below 8x10^-6 Torr. Does not change errors in the range of 10^-2 torr or above")

        self.commands['atmospheric_adjust'] = self.__MKS_msg("!?", "ATM", "\d\.\d{3}E[+-]\d",
        "Change the atmospheric adjustment of the machine. Must be done at atmospheric pressure, and can only be executed with air or nitrogen")

        #Lock And Test Commands
        self.commands['lock'] = self.__MKS_msg("!","FD","(UN)?LOCK",
        "Prevents modification of other settings untill disabled. Kinda silly, I guess")

        self.commands['lock_display'] = self.__MKS_msg("?!", "SW", "(ON)|(OFF)", 
        "Disables adjustment of zero and atmospheric adjustments, by disabiling the User Switch function")

        self.commands['test_blink'] = self.__MKS_msg("?!", "TST", "(ON)|(OFF)",
        "Enables or disables the flashing of the onboard LED for identification purpouses")

        self.commands['device_type'] = self.__MKS_msg("?", "DT", "", "Get Device Type Name")
        self.commands['firmware_ver'] = self.__MKS_msg("?", "FV", "", "Get Firmware Version")
        self.commands['manufacturer'] = self.__MKS_msg("?", "MF", "", "Get Device Manufacturer")
        self.commands['model_number'] = self.__MKS_msg("?", "MD", "", "Get Transducer Model Number")
        self.commands['part_number'] = self.__MKS_msg("?", "PN", "", "Get Transducer Part Number")
        self.commands['serial_num'] = self.__MKS_msg("?", "SN", "", "Get Transducer Serial Number")
        self.commands['uptime'] = self.__MKS_msg("?", "TIM", "", "Get number of hours the transducer has been on")
        self.commands['temperature'] = self.__MKS_msg("?", "TEM", "", "Get On-Chip Temperature Reading")
        self.commands['status'] = self.__MKS_msg("?", "TEM", "", "Get Status, O for ok, M for fail")

       ################# CLASS SETUP ################## 


        # Set up vars and create serial port
        self.baudrate = baud
        self.serialport = port
        self.address = adr
        self.serialport = serial.Serial(self.serialport, 
                                        self.baudrate)

        # The three externaly accessable wrapper objects, for the two different things
        # you can do with MKS messages: Make Queries, or Send commands. Docs are accessed in the standard python manner.
        self.query      = self.__MKS_wrapper( com for com in self.commands if "?" in com.msg_types)
        self.set        = self.__MKS_wrapper( com for com in self.commands if "!" in com.msg_types)



from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class LkshtempStreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(LkshtempStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        # Note: Many commands exist in the operations manual that are not included in this emulator,
        # as they are considered unnecessary to the operation of the device in our EPICS ecosystem
        self.commands = {
            # Common Commands

            # Getters
            CmdBuilder(self.get_id).escape("*IDN?").eos().build(),  # Get ID
            CmdBuilder(self.get_aout).escape("AOUT? ").int().eos().build(), # Analog Output Data Query; Returns the percentage of output of the analog output.        
            CmdBuilder(self.get_setp).escape("SETP? ").int().eos().build(), # Get Setpoint 
            CmdBuilder(self.get_cmode).escape("CMODE? ").int().eos().build(),  # Get CMODE
            CmdBuilder(self.get_tempK).escape("KRDG? ").string().eos().build(),  # Get Temperature reading in Kelvin
            CmdBuilder(self.get_tempC).escape("CRDG? ").string().eos().build(),  # Get Temperature reading in Celsius
            CmdBuilder(self.get_srdg).escape("SRDG? ").string().eos().build(), #Sensor Units Input Reading Query 
            CmdBuilder(self.get_range).escape("RANGE? ").int().eos().build(), # Get Output Range 
            CmdBuilder(self.catch_all).arg("^#9.*$").build(),  # Catch-all command for debugging
            CmdBuilder(self.get_htr).escape("HTR? ").int().eos().build(), # Get Heater readout
            CmdBuilder(self.get_ramp).escape("RAMP? ").int().eos().build(), # Control Loop Ramp Query
            CmdBuilder(self.get_mout).escape("MOUT? ").int().eos().build(), # Control Loop MHP Output Query            
            CmdBuilder(self.get_pid).escape("PID? ").int().eos().build(), # Control Loop PID Values Query
            CmdBuilder(self.get_alarmst).escape("ALARMST? ").string().eos().build(), # Input Alarm Status Query
            CmdBuilder(self.get_alarm).escape("ALARM? ").string().eos().build(), # Input Alarm Parameter Query
            CmdBuilder(self.get_rdgst).escape("RDGST? ").string().eos().build(), #Input Status Query
            CmdBuilder(self.get_htrst).escape("HTRST? ").int().eos().build(), # Heater Status Query
            CmdBuilder(self.get_incrv).escape("INCRV? ").string().eos().build(), # Input Curve Number Query
            CmdBuilder(self.get_crvhdr).escape("CRVHDR? ").int().eos().build(), # Curve Header Query
            CmdBuilder(self.get_intype).escape("INTYPE? ").string().eos().build(), # Input Type Parameter Query

            # Setters
                                                             
            CmdBuilder(self.set_tset).escape("SETP ").int().escape(",").float().eos().build(), # Set Setpoint
            CmdBuilder(self.set_range).escape("RANGE ").int().escape(",").int().eos().build(), # Set Heater Range
            CmdBuilder(self.set_ramp).escape("RAMP ").int().escape(",").int().escape(",").float().eos().build(), #Control Loop Ramp Cmd
            CmdBuilder(self.set_mout).escape("MOUT ").int().escape(",").float().eos().build(), # Control Loop MHP Output Cmd
            CmdBuilder(self.set_pid).escape("PID ").int().escape(",").float().escape(",").float().escape(",").float().eos().build(), # Control Loop PID Values Cmd
            CmdBuilder(self.set_crvhdr).escape("CRVHDR ").int().escape(",").string().escape(",")string().escape(",").int().escape(",").float().escape(",").int().eos().build(), # Curve Header Cmd,

        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
    
    ########## Getters ######################

    @conditional_reply("connected")
    def get_id(self):
        return "LSCI,{}".format(self.device.id)

    @conditional_reply("connected")
    def get_tempK(self, output):
        return self.device.get_output_setpoint(output)

    @conditional_reply("connected")
    def get_tempC(self, output):
        return self.device.get_output_setpoint(output)

    @conditional_reply("connected")
    def get_cmode(self, output):
        return self.device.get_cmode(output)
    
    @conditional_reply("connected")
    def get_range(self, output):
        return self.device.get_output_range(output)

    @conditional_reply("connected")
    def get_htr(self, output):
        return self.device.get_output_heater_value(output)
    
    @conditional_reply("connected")
    def get_aout(self, output):
        return self.device.get_output_analog_output(output)

    @conditional_reply("connected")
    def get_setp(self, output):
        return self.device.get_output_setpoint(output)

    @conditional_reply("connected")
    def get_krdg(self, input):
        return self.device.get_input_kelvin_temperature(input)

    @conditional_reply("connected")
    def get_srdg(self, input):
        return self.device.get_input_voltage_input(input)

    @conditional_reply("connected")
    def get_ramp(self, output):
        return self.device.get_output_ramp(output)

    @conditional_reply("connected")
    def get_mout(self, output):
        return self.device.get_output_manual_value(output)

    @conditional_reply("connected")
    def get_pid(self, output):
        return self.device.get_pid(output)

    @conditional_reply("connected")
    def get_om(self, output):
        return self.device.get_output_mode(output)

    @conditional_reply("connected")
    def get_alarmst(self, input):
        return self.device.get_input_alarm_status(input)

    @conditional_reply("connected")
    def get_alarm(self, input):
        return self.device.get_input_alarm(input)

    @conditional_reply("connected")
    def get_rdgst(self, input):
        return self.device.get_input_reading_status(input)

    @conditional_reply("connected")
    def get_htrst(self, output):
        return self.device.get_output_heater_status(output)

    @conditional_reply("connected")
    def get_incrv(self, input):
        return self.device.get_input_curve_number(input)

    @conditional_reply("connected")
    def get_crvhdr(self, _):
        return self.device.get_input_curve_header()

    @conditional_reply("connected")
    def get_intype(self, input):
        return self.device.get_input_type(input)

    ########## Setters ######################

    @conditional_reply("connected")
    def set_setp(self, output, value):
        self.device.set_output_setpoint(output, value)

    @conditional_reply("connected")
    def set_range(self, output, value):
        self.device.set_output_range(output, value)

    @conditional_reply("connected")
    def set_ramp(self, output, status, rate):
        self.device.set_output_ramp(output, status, rate)

    @conditional_reply("connected")
    def set_mout(self, output, value):
        self.device.set_output_manual_value(output, value)

    @conditional_reply("connected")
    def set_pid(self, output, p, i, d):
        self.device.set_pid(output, p, i, d)

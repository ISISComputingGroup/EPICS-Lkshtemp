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
        self.commands = {
            # Getters
            CmdBuilder(self.get_id).escape("*IDN?").eos().build(),  # Get ID
            CmdBuilder(self.get_aout).escape("AOUT? ").int().eos().build(), # Analog Output Data Query; Returns the percentage of output of the analog output.        
            CmdBuilder(self.get_setp).escape("SETP? ").int().eos().build(), # Get Setpoint 
            CmdBuilder(self.get_cmode).escape("CMODE? ").int().eos().build(),  # Get CMODE
            CmdBuilder(self.get_temp).escape("*KRDG? ").string().eos().build(),  # Get Temperature reading in Kelvin
            CmdBuilder(self.get_srdg).escape("SRDG? ").string().eos().build(), #Sensor Units Input Reading Query 
            CmdBuilder(self.get_range).escape("RANGE? ").int().eos().build(), # Get Output Range 
            CmdBuilder(self.catch_all).arg("^#9.*$").build(),  # Catch-all command for debugging
            CmdBuilder(self.get_htr).escape("HTR? ").int().eos().build(), # Get Heater readout
            CmdBuilder(self.get_srdg).escape("SRDG? ").string().eos().build(), # Get Sensort Measure Units
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
            



            #########################
            # 336 Commands

            CmdBuilder(self.get_om).escape("OUTMODE? ").int().eos().build(),
            CmdBuilder(self.get_inname).escape("INNAME? ").string().eos().build(),
            
            

            
            
            
            CmdBuilder(self.set_outmode).escape("OUTMODE ").int().escape(",").int().escape(",").int().escape(",").int().eos().build(),
            CmdBuilder(self.set_inname).escape("INNAME ").string().escape(",").escape('"').string().escape('"').eos().build()

        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        pass

    def get_id(self):
        return "LSCI,{}".format(self.device.id)
    
    def get_temp(self, output):
        return self.device.get_output_setpoint(output)

    def get_cmode(self, output):
        return self.device.get_cmode(output)
    
    def get_range(self, output):
        return self.device.get_output_range(output)
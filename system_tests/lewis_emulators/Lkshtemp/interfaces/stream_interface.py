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
            CmdBuilder(self.catch_all).arg("^#9.*$").build(),  # Catch-all command for debugging
            CmdBuilder(self.get_temp).escape("*KRDG? ").string().eos().build(),  # Get Temperature reading in Kelvin
            CmdBuilder(self.get_id).escape("*IDN?").eos().build(),  # Get ID
            CmdBuilder(self.get_cmode).escape("CMODE? ").int().eos().build(),  # Get CMODE
            CmdBuilder(self.get_range).escape("RANGE? ").int().eos().build(),  # Get Output Range
            CmdBuilder(self.get_setp).escape("SETP? ").int().eos().build(), # Get Setpoint
            CmdBuilder(self.get_htr).escape("HTR? ").int().eos().build(), # Get Heater readout
            CmdBuilder(self.get_srdg).escape("SRDG? ").string().eos().build(), # Get Sensort Measure Units


            CmdBuilder(self.set_tset).escape("SETP ").int().escape(",").float().eos().build(), # Set Setpoint
            CmdBuilder(self.set_range).escape("RANGE ").int().escape(",").int().eos().build(), # Set Heater Range

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
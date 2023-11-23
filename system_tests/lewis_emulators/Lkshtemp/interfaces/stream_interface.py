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
            # Common Commands

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
            
            # Getters
            CmdBuilder(self.get_om).escape("OUTMODE? ").int().eos().build(),
            CmdBuilder(self.get_inname).escape("INNAME? ").string().eos().build(),
            
            # Setters
            CmdBuilder(self.set_outmode).escape("OUTMODE ").int().escape(",").int().escape(",").int().escape(",").int().eos().build(),
            CmdBuilder(self.set_inname).escape("INNAME ").string().escape(",").escape('"').string().escape('"').eos().build(),

            #########################
            # 340 Commands

            CmdBuilder("get_temperature_a").escape("KRDG? 0").eos().build(),
            CmdBuilder("get_temperature_b").escape("KRDG? 1").eos().build(),
            CmdBuilder("get_temperature_c").escape("KRDG? 2").eos().build(),
            CmdBuilder("get_temperature_d").escape("KRDG? 3").eos().build(),

            CmdBuilder("get_measurement_a").escape("SRDG? 0").eos().build(),
            CmdBuilder("get_measurement_b").escape("SRDG? 1").eos().build(),
            CmdBuilder("get_measurement_c").escape("SRDG? 2").eos().build(),
            CmdBuilder("get_measurement_d").escape("SRDG? 3").eos().build(),

            CmdBuilder("set_tset").escape("SETP {},".format(_CONTROL_CHANNEL_INDEX)).float().eos().build(),
            CmdBuilder("get_tset").escape("SETP? {}".format(_CONTROL_CHANNEL_INDEX)).eos().build(),

            CmdBuilder("set_pid").escape("PID {},".format(_CONTROL_CHANNEL_INDEX)).float().escape(",").float().escape(",").int().eos().build(),
            CmdBuilder("get_pid").escape("PID? {}".format(_CONTROL_CHANNEL_INDEX)).eos().build(),

            CmdBuilder("set_pid_mode").escape("CMODE {},".format(_CONTROL_CHANNEL_INDEX)).int().eos().build(),
            CmdBuilder("get_pid_mode").escape("CMODE? {}".format(_CONTROL_CHANNEL_INDEX)).eos().build(),

            CmdBuilder("set_control_mode")
            .escape("CSET {},{},{},".format(_CONTROL_CHANNEL_INDEX, _CONTROL_CHANNEL, _SENSOR_UNITS)).int()
            .escape(",{}".format(_POWERUPENABLE)).eos().build(),
            CmdBuilder("get_control_mode").escape("CSET? {}".format(_CONTROL_CHANNEL_INDEX)).eos().build(),

            CmdBuilder("set_temp_limit").escape("CLIMIT {},".format(_CONTROL_CHANNEL_INDEX)).float().eos().build(),
            CmdBuilder("get_temp_limit").escape("CLIMIT? {}".format(_CONTROL_CHANNEL_INDEX)).eos().build(),

            CmdBuilder("get_heater_output").escape("HTR?").eos().build(),

            CmdBuilder("set_heater_range").escape("RANGE ").int().eos().build(),
            CmdBuilder("get_heater_range").escape("RANGE?").eos().build(),

            CmdBuilder("get_excitation_a").escape("INTYPE? A").eos().build(),
            CmdBuilder("set_excitation_a").escape("INTYPE A, 1, , , , ").int().eos().build(),

            #########################
            # 372 Commands

            CmdBuilder("get_tset").escape("SETP? 0").eos().build(),
            CmdBuilder("set_tset").escape("SETP 0 ").float().eos().build(),
            CmdBuilder("get_temperature").escape("RDGK? A").eos().build(),
            CmdBuilder("get_resistance").escape("RDGR? A").eos().build(),

            CmdBuilder("get_heater_range").escape("RANGE? 0").eos().build(),
            CmdBuilder("set_heater_range").escape("RANGE 0,").int().eos().build(),

            CmdBuilder("get_heater_power").escape("HTR?").eos().build(),

            CmdBuilder("get_pid").escape("PID? ").optional("0").eos().build(),
            CmdBuilder("set_pid").escape("PID ").float().escape(",").float().escape(",").float().eos().build(),

            CmdBuilder("get_outmode").escape("OUTMODE? 0").eos().build(),
            CmdBuilder("set_outmode").escape("OUTMODE 0,").int().escape(",").int().escape(",").int().escape(",").int().escape(",").int().escape(",").int().eos().build(),
    

        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
    
    ########## 332 ######################

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
    
    ########## 336 ######################

    @conditional_reply("connected")
    def get_id(self):
        return "LSCI,{}".format(self.device.id)

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
    def get_range(self, output):
        return self.device.get_output_range(output)

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
    def get_inname(self, input):
        return self.device.get_input_sensor_name(input)

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

    @conditional_reply("connected")
    def set_outmode(self, output, mode, control_input, powerup):
        self.device.set_output_mode(output, mode, control_input, powerup)

    @conditional_reply("connected")
    def set_inname(self, input, value):
        self.device.set_input_sensor_name(input, value)

########## 340 ######################   

    def get_temperature_a(self):
        return self._device.temp_a

    def get_temperature_b(self):
        return self._device.temp_b

    def get_temperature_c(self):
        return self._device.temp_c

    def get_temperature_d(self):
        return self._device.temp_d

    def get_measurement_a(self):
        return self._device.measurement_a

    def get_measurement_b(self):
        return self._device.measurement_b

    def get_measurement_c(self):
        return self._device.measurement_c

    def get_measurement_d(self):
        return self._device.measurement_d

    def set_tset(self, val):
        self._device.tset = float(val)

    def get_tset(self):
        return self._device.tset

    def set_pid(self, p, i, d):
        self._device.p, self._device.i, self._device.d = p, i, d

    def get_pid(self):
        return "{},{},{}".format(self._device.p, self._device.i, self._device.d)

    def get_pid_mode(self):
        return self._device.pid_mode

    def set_pid_mode(self, mode):
        if not 1 <= mode <= 6:
            raise ValueError("Mode must be 1-6")
        self._device.pid_mode = mode

    def get_control_mode(self):
        return "{},{},{},{}".format(_CONTROL_CHANNEL, _SENSOR_UNITS, 1 if self._device.loop_on else 0, _POWERUPENABLE)

    def set_control_mode(self, val):
        self._device.loop_on = bool(val)

    def set_temp_limit(self, val):
        self._device.max_temp = val

    def get_temp_limit(self):
        return "{},0,0,0,0".format(self._device.max_temp)

    def get_heater_output(self):
        return "{:.2f}".format(self._device.heater_output)

    def get_heater_range(self):
        return self._device.heater_range

    def set_heater_range(self, val):
        if not 0 <= val <= 5:
            raise ValueError("Heater range must be 0-5")
        self._device.heater_range = val

    def get_excitation_a(self):
        return self._device.excitationa

    def set_excitation_a(self, val):
        if not 0 <= val <= 12:
            raise ValueError("Excitations range must be 0-12")
        self._device.excitationa = val

########## 372 ######################

    def set_tset(self, temperature):
            self._device.temperature = temperature

    @if_connected
    def get_tset(self):
        return "{:.3f}".format(self._device.temperature)

    @if_connected
    def get_temperature(self):
        return "{:.3f}".format(self._device.temperature)

    @if_connected
    def get_resistance(self):
        return "{:.6f}".format(self._device.sensor_resistance)

    def set_heater_range(self, heater_range):
        self._device.heater_range = heater_range

    @if_connected
    def get_heater_range(self):
        return "{:d}".format(self._device.heater_range)

    @if_connected
    def get_heater_power(self):
        return "{:.3f}".format(self._device.heater_power)

    @if_connected
    def get_pid(self):
        return "{:.6f},{:d},{:d}".format(self._device.p, self._device.i, self._device.d)

    def set_pid(self, p, i, d):
        self._device.p = p
        self._device.i = int(round(i))
        self._device.d = int(round(d))

    @if_connected
    def get_outmode(self):
        return "{:d},{:d},{:d},{:d},{:d},{:d}".format(self._device.control_mode, OUTMODE_INPUT, OUTMODE_POWERUPENABLE,
                                                      OUTMODE_POLARITY, OUTMODE_FILTER, OUTMODE_DELAY)

    def set_outmode(self, control_mode, inp, powerup_enable, polarity, filt, delay):
        if inp != OUTMODE_INPUT or powerup_enable != OUTMODE_POWERUPENABLE or polarity != OUTMODE_POLARITY or filt != OUTMODE_FILTER or delay != OUTMODE_DELAY:
            raise ValueError("Invalid parameters sent to set_outmode")
        self._device.control_mode = control_mode

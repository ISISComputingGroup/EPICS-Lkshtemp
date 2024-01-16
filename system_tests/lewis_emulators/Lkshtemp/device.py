from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


NUM_OUTPUTS = 2
INPUTS = ['A', 'B']


class CurveHeader(object):
    """
    Class representing the header information of a curve.
    """
    def __init__(self):
        # Needs to be 15 characters.
        self.name = "".rjust(15, "#")
        # Needs to be 10 characters.
        self.serial_number = "".rjust(10, "#")
        self.data_format = 0
        self.temperature_limit = 0.0
        self.temperature_coefficient = 0
        
class Outputs(object):
    """
    Class holding all of the output variables.
    """
    def __init__(self) -> None:
        self.heater_value = 0
        self.analog_output = 0
        self.setpoint = 0.0
        self.range = 0
        self.ramp_rate = 0.0
        self.ramp_status = 0
        self.manual_value = 0.0
        self.p = 0
        self.i = 0
        self.d = 0
        self.mode = 0
        self.control_input = 0
        self.powerup = 0
        self.heater_status = 0

class Inputs(object):
    """
    Class holding all of the input variables.
    """
    def __init__(self) -> None:
        self.kelvin_temperature = 0
        self.voltage_input = 0
        self.sensor_name = ""
        self.alarm_high = 0
        self.alarm_low = 0
        self.alarm_enabled = 0
        self.alarm_high_setpoint = 0
        self.alarm_low_setpoint = 0
        self.alarm_deadband = 0
        self.alarm_latching = 0
        self.alarm_audible = 0
        self.alarm_visible = 0
        self.reading_status = 0
        self.curve_number = 0
        self.sensor_type = 0
        self.auto_range_setting = 0
        self.range = 0
        self.compensation = 0
        self.units = 0

class SimulatedLksh336(StateMachineDevice):

    def _initialize_data(self):
        self.connected = True

        self.id = ""
        self.outputs = [Outputs()] * NUM_OUTPUTS
        self.inputs = { k:v for k,v in zip(INPUTS, [Inputs()] * len(INPUTS)) }
        self.input_curve_header = CurveHeader()
        
        
    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])


    def get_output_heater_value(self, output):
        return self.outputs[output - 1].heater_value

    def get_output_analog_output(self, output):
        return self.outputs[output - 1].analog_output

    def get_output_setpoint(self, output):
        return self.outputs[output - 1].setpoint

    def get_input_kelvin_temperature(self, input):
        return self.inputs[input].kelvin_temperature

    def get_input_voltage_input(self, input):
        return self.inputs[input].voltage_input

    def get_output_range(self, output):
        return self.outputs[output - 1].range

    def get_output_ramp(self, output):
        ouput = self.outputs[output - 1]
        return f"{ouput.ramp_status},{ouput.ramp_rate}"

    def get_output_manual_value(self, output):
        return self.outputs[output - 1].manual_value

    def get_pid(self, output):
        output = self.outputs[output - 1]
        return f"{output.p},{output.i},{output.d}"

    def get_output_mode(self, output):
        output = self.outputs[output - 1]
        return f"{output.mode},{output.control_input},{output.powerup}"

    def get_input_sensor_name(self, input):
        return self.inputs[input].sensor_name

    def get_input_alarm_status(self, input):
        input = self.inputs[input]
        return f"{input.alarm_high},{input.alarm_low}"

    def get_input_alarm(self, input):
        input = self.inputs[input]
        return "{},{},{},{},{},{},{}".format(
            input.alarm_enabled,
            input.alarm_high_setpoint,
            input.alarm_low_setpoint,
            input.alarm_deadband,
            input.alarm_latching,
            input.alarm_audible,
            input.alarm_visible
        )

    def get_input_reading_status(self, input):
        return self.inputs[input].reading_status

    def get_output_heater_status(self, output):
        return self.outputs[output - 1].heater_status

    def get_input_curve_number(self, input):
        return self.inputs[input].curve_number

    def get_input_curve_header(self):
        return "{},{},{},{},{}".format(
            self.input_curve_header.name,
            self.input_curve_header.serial_number,
            self.input_curve_header.data_format,
            self.input_curve_header.temperature_limit,
            self.input_curve_header.temperature_coefficient
        )

    def get_input_type(self, input):
        input = self.inputs[input]
        return f"{input.sensor_type},{input.auto_range_setting},{input.range},{input.compensation},{input.units}"


    def set_output_heater_value(self, output, value):
        self.outputs[output - 1].heater_value = value

    def set_output_analog_output(self, output, value):
        self.outputs[output - 1].analog_output = value

    def set_output_setpoint(self, output, value):
        self.outputs[output - 1].setpoint = value

    def set_input_kelvin_temperature(self, input, value):
        self.inputs[input].kelvin_temperature = value

    def set_input_voltage_input(self, input, value):
        self.inputs[input].voltage_input = value

    def set_output_range(self, output, value):
        self.outputs[output - 1].range = value

    def set_output_ramp(self, output, status, rate):
        output = self.outputs[output - 1]
        output.ramp_status = status
        output.ramp_rate = rate

    def set_output_manual_value(self, output, value):
        self.outputs[output - 1].manual_value = value

    def set_pid(self, output, p, i, d):
        output = self.outputs[output - 1]
        output.p = p
        output.i = i
        output.d = d

    def set_output_mode(self, output, mode, control_input, powerup):
        output = self.outputs[output - 1]
        output.mode = mode
        output.control_input = control_input
        output.powerup = powerup

    def set_input_sensor_name(self, input, value):
        self.inputs[input].sensor_name = value

    def set_input_alarm_status(self, input, high, low):
        input = self.inputs[input]
        input.alarm_high = high
        input.alarm_low = low

    def set_input_alarm(self, input, enabled, high_setpoint, low_setpoint, deadband, latching, audible, visible):
        input = self.inputs[input]
        input.alarm_enabled = enabled
        input.alarm_high_setpoint = high_setpoint
        input.alarm_low_setpoint = low_setpoint
        input.alarm_deadband = deadband
        input.alarm_latching = latching
        input.alarm_audible = audible
        input.alarm_visible = visible

    def set_input_reading_status(self, input, value):
        self.inputs[input].reading_status = value

    def set_output_heater_status(self, output, value):
        self.outputs[output - 1].heater_status = value

    def set_input_curve_number(self, input, value):
        self.inputs[input].curve_number = value

    def set_input_curve_header(self, _, name, serial_number, data_format, temperature_limit, temperature_coefficient):
        self.input_curve_header.name = name
        self.input_curve_header.serial_number = serial_number
        self.input_curve_header.data_format = data_format
        self.input_curve_header.temperature_limit = temperature_limit
        self.input_curve_header.temperature_coefficient = temperature_coefficient

    def set_input_type(self, input, sensor_type, auto_range_setting, range, compensation, units):
        input = self.inputs[input]
        input.sensor_type = sensor_type
        input.auto_range_setting = auto_range_setting
        input.range = range
        input.compensation = compensation
        input.units = units


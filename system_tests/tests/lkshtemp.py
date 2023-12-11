import contextlib
import unittest

from parameterized import parameterized

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, parameterized_list, skip_if_recsim


DEVICE_PREFIX = "LKSH336_01"

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LKSHTEMP"),
        "macros": {},
        "emulator": "Lkshtemp",
    },
]

TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


OUTPUTS = [ 1, 2]
INPUTS = ['A', 'B']
ALARM_PVS = [
    "HEATER1:OUTPUT",
    "HEATER2:OUTPUT",
    
    "TEMP1:SP:RBV",
    "TEMP2:SP:RBV",
    
    "TEMP_A",
    "TEMP_B",
    
]

class Lksh336Tests(unittest.TestCase):
    """
    Tests for the Lkshtemp IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Lkshtemp", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0)

    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_id_set_via_backdoor_THEN_id_updates(self):
        self._lewis.backdoor_set_on_device("id", "test")
        self.ca.process_pv("ID")
        self.ca.assert_that_pv_is("ID", "test")
    
    @parameterized.expand(
        [("heater_value", i, f"HEATER{i}:OUTPUT") for i in range(1,3)] +
        [("analog_output", j, f"HEATER{j}:OUTPUT") for j in range (3,5)]
    )
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_output_set_via_backdoor_THEN_output_value_updates(self, output_type, output, pv):
        self._lewis.backdoor_command(["device", f"set_output_{output_type}", str(output), str(2)])
        self.ca.assert_that_pv_is(pv, 2)
    
    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_output_setpoint_set_THEN_output_setpoint_updates(self, _, output):
        self.ca.set_pv_value(f"TEMP{output}:SP", 2.0)
        self.ca.assert_that_pv_is(f"TEMP{output}:SP:RBV", 2.0)

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_kelvin_temperature_set_via_backdoor_THEN_input_kelvin_temperature_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_kelvin_temperature", input, str(2)])
        self.ca.assert_that_pv_is(f"TEMP_{input}", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_voltage_input_set_via_backdoor_THEN_input_voltage_input_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_voltage_input", input, str(2)])
        self.ca.assert_that_pv_is(f"RAW_VOLT_{input}", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_output_range_set_THEN_output_range_updates(self, _, output):
        self.ca.set_pv_value(f"HEATER{output}:RANGE:SP", 2)
        self.ca.assert_that_pv_is(f"HEATER{output}:RANGE", "Medium")

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_output_ramp_set_THEN_output_ramp_updates(self, _, output):
        self.ca.set_pv_value(f"RAMP_RATE{output}:SP", 2.0)
        self.ca.assert_that_pv_is(f"RAMP_RATE{output}", 2.0)
        self.ca.set_pv_value(f"RAMP_ON{output}:SP", 1)
        self.ca.assert_that_pv_is(f"RAMP_ON{output}", "On")

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_output_manual_value_set_THEN_output_manual_value_updates(self, _, output):
        self.ca.set_pv_value(f"MANUAL_OUT{output}:SP", 2.0)
        self.ca.assert_that_pv_is(f"MANUAL_OUT{output}", 2.0)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_pid_set_THEN_pid_updates(self, _, output):
        self.ca.set_pv_value(f"P{output}:SP", 1.0)
        self.ca.assert_that_pv_is(f"P{output}", 1.0)
        self.ca.set_pv_value(f"I{output}:SP", 2.0)
        self.ca.assert_that_pv_is(f"I{output}", 2.0)
        self.ca.set_pv_value(f"D{output}:SP", 3.0)
        self.ca.assert_that_pv_is(f"D{output}", 3.0)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_WHEN_output_mode_set_THEN_output_mode_updates(self, _, output):
        self.ca.set_pv_value(f"OUT_MODE{output}:SP", 2)
        self.ca.assert_that_pv_is(f"OUT_MODE{output}", "Zone")
        self.ca.set_pv_value(f"CTRL_IN{output}:SP", 2)
        self.ca.assert_that_pv_is(f"CTRL_IN{output}", "Measurement B")
        self.ca.set_pv_value(f"POWERUP{output}:SP", 1)
        self.ca.assert_that_pv_is(f"POWERUP{output}", "On")

    @parameterized.expand(parameterized_list(INPUTS))
    def test_WHEN_input_sensor_name_set_THEN_input_sensor_name_updates(self, _, input):
        self.ca.set_pv_value(f"NAME_{input}:SP", "test")
        self.ca.assert_that_pv_is(f"NAME_{input}", "test")

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_alarm_status_set_via_backdoor_THEN_input_alarm_status_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_alarm_status", input, str(1), str(1)])
        self.ca.assert_that_pv_is(f"ALARM_{input}:HIGH", "On")
        self.ca.assert_that_pv_is(f"ALARM_{input}:LOW", "On")

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_alarm_set_via_backdoor_THEN_input_alarm_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_alarm", input, str(1), str(2), str(2), str(2), str(1), str(1), str(1)])
        self.ca.assert_that_pv_is(f"ALARM_{input}:ON", "Enabled")
        self.ca.assert_that_pv_is(f"ALARM_{input}:HIVAL", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:LOVAL", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:DEADBAND", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:LATCHED", "Latching")
        self.ca.assert_that_pv_is(f"ALARM_{input}:AUDIBLE", "Audible")
        self.ca.assert_that_pv_is(f"ALARM_{input}:VISIBLE", "Visible")

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_reading_status_set_via_backdoor_THEN_input_reading_status_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_reading_status", input, str(2)])
        self.ca.assert_that_pv_is(f"READING_{input}:STAT", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_output_heater_status_set_via_backdoor_THEN_output_heater_status_updates(self, _, output):
        self._lewis.backdoor_command(["device", "set_output_heater_status", str(output), str(2)])
        self.ca.assert_that_pv_is(f"HEATER{output}:RAW_STAT", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_curve_number_set_via_backdoor_THEN_input_curve_number_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_curve_number", input, str(2)])
        self.ca.assert_that_pv_is(f"CURVE_{input}:NUM", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_curve_header_set_via_backdoor_THEN_input_curve_header_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_curve_header", str(0), "name".rjust(15, "a"), "num".rjust(10, "a"), str(2), str(2.0), str(2)])
        self.ca.assert_that_pv_is(f"CURVE_{input}:NAME", "name".rjust(15, "a"))
        self.ca.assert_that_pv_is(f"CURVE_{input}:SERIAL_N", "num".rjust(10, "a"))
        self.ca.assert_that_pv_is(f"CURVE_{input}:FORMAT", "V/K")
        self.ca.assert_that_pv_is(f"CURVE_{input}:LIM", 2.0)
        self.ca.assert_that_pv_is(f"CURVE_{input}:COEFF", "Positive")

    @parameterized.expand(parameterized_list(INPUTS))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_input_type_set_via_backdoor_THEN_input_type_updates(self, _, input):
        self._lewis.backdoor_command(["device", "set_input_type", input, str(2), str(1), str(2), str(1), str(2)])
        self.ca.assert_that_pv_is(f"IN_{input}:SENS_TYPE", "Platinum RTD")
        self.ca.assert_that_pv_is(f"IN_{input}:AUTORANGE", "On")
        self.ca.assert_that_pv_is(f"IN_{input}:RANGE", "100 Ohm")
        self.ca.assert_that_pv_is(f"IN_{input}:COMPENSATION", "On")
        self.ca.assert_that_pv_is(f"IN_{input}:UNITS", "Celcius")

    @contextlib.contextmanager
    def _disconnect_device(self):
        self._lewis.backdoor_set_on_device("connected", False)
        try:
            yield
        finally:
            self._lewis.backdoor_set_on_device("connected", True)

    @parameterized.expand(parameterized_list(ALARM_PVS))
    @skip_if_recsim("Need emulator to test disconnected behaviour")
    def test_WHEN_device_disconnected_THEN_go_into_alarm(self, _, alarm_pv):
        # A long timeout is needed to handle the lewis backdoor command timing.
        self.ca.assert_that_pv_alarm_is(alarm_pv, self.ca.Alarms.NONE, timeout=30)

        with self._disconnect_device():
            self.ca.assert_that_pv_alarm_is(alarm_pv, self.ca.Alarms.INVALID, timeout=30)

        self.ca.assert_that_pv_alarm_is(alarm_pv, self.ca.Alarms.NONE, timeout=30)

import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim


DEVICE_PREFIX = "LKSHTEMP_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LKSHTEMP"),
        "macros": {},
        "emulator": "Lkshtemp",
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


class LkshtempTests(unittest.TestCase):
    """
    Tests for the Lkshtemp IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Lkshtemp", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    def test_that_fails(self):
        self.fail("You haven't implemented any tests!")

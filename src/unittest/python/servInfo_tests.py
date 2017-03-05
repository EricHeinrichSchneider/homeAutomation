import unittest
from util.serverUtil import serverUtil
import re

class TestServerInfo(unittest.TestCase):

    def setUp(self):
        self.sI = serverUtil()

    def test_serverTime(self):
        sTime = self.sI.getServerTime()
        p = re.compile('^\d{3}:\d{2}:\d{2}:\d{2}.\d{6}$')
        #if there is a match object then the value is according to the pattern
        self.assertIsNotNone(p.match(sTime))

    def test_load(self):
        result = self.sI.getLoadAvg()
        # Returned values
        self.assertIsNotNone(result)
        # should be 3
        self.assertEqual(len(result),3)

import unittest
from util.serverUtil import serverUtil
import re

class TestServerInfo(unittest.TestCase):

    def setUp(self):
        self.sI = serverUtil()

    def test_serverTime(self):
        sTime = self.sI.getServerTime()
        print(sTime)
        p = re.compile('^\d{3}:\d{2}:\d{2}:\d{2}.\d{6}$')
        assert p.match(sTime) != None

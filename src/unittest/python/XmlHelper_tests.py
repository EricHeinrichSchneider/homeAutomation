from util.xmlConfigReader import XmlHelper
import unittest
from mockito import verify
from mockito import when
import os

class TestXmlHelper(unittest.TestCase):

    def setUp(self):
        XmlHelper.configPath = "./src/unittest/res/unitTest.config"
        self.xmlH = XmlHelper()

    def test_root(self):
        self.assertIsNotNone(self.xmlH.getRoot())

    def test_serverInfo(self):
        res = self.xmlH.getServerInfo()
        self.assertIsNotNone(res)
        self.assertEqual(res["name"],"The Servername")
        self.assertEqual(res["latitude"],"55.5")
        self.assertEqual(res["longitude"],"-44.4233")

    def test_getActuator(self):
        res = self.xmlH.getActuator("1")
        self.assertEqual(res.attrib.get("name"),"Test actuator1")

    def test_getActuatorAction(self):
        res = self.xmlH.getActuatorAction("1","on")
        self.assertIsNotNone(res)

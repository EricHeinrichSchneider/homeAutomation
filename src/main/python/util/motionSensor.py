import time
import datetime
import logging
from util.gpioUtil import GPIOUtil
import RPi.GPIO as GPIO
from util.eventDBLog import EventDBLog


class MotionSensor:
    def __init__(self):
        self.pin = 17
        self.dbLog = EventDBLog()

    def setPin(self,pin):
        self.pin =pin

    def initSensor(self):
        logging.debug("Init MotionSensor event")
        GPIOUtil().addEvent(self.pin,GPIO.RISING,self.callback);

    def callback(self,channel):
        logging.debug("Event at Motion sensor")
        self.dbLog.logSensorEvent("Motion Sensor",datetime.datetime.now())

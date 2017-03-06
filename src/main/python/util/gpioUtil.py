import RPi.GPIO as GPIO
import time
import logging

class GPIOUtil:
    instance = None

    class ____GPIOUtil:
        #delays for the signal, signallength etc..
        short_delay = 0.00015
        long_delay = 0.00045
        extended_delay = 0.0047
        #which pin on the pi and how many attempts
        NUM_ATTEMPTS = 10

        def __init__(self):
            GPIO.setwarnings(False) #TODO remove - check why it comes to error
            GPIO.setmode(GPIO.BCM)

        def transmit_code(self,transmptPin,code):
            '''Transmit a chosen code string using the GPIO transmitter'''
            logging.debug("transmit_code " + str(transmptPin) + " - " + code )
            GPIO.setup(transmptPin,GPIO.OUT)
            for t in range(self.NUM_ATTEMPTS):
            	for i in code:
            		if i == '1':
            			GPIO.output(transmptPin, 1)
            			time.sleep(self.short_delay)
            			GPIO.output(transmptPin, 0)
            			time.sleep(self.long_delay)
            		elif i == '0':
            			GPIO.output(transmptPin, 1)
            			time.sleep(self.long_delay)
            			GPIO.output(transmptPin, 0)
            			time.sleep(self.short_delay)
            		else:
            			continue
            	GPIO.output(transmptPin, 0)
            	time.sleep(self.extended_delay)
            return None

        def addEvent(self,pin,edge,callBack):
            logging.debug("add Event" + str(pin) + " " + str(callBack) )
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=callBack, bouncetime=300)

        @staticmethod
        def cleanUP():
            GPIO.cleanup()


    def __init__(self):
    	if not GPIOUtil.instance:
    		GPIOUtil.instance = GPIOUtil.____GPIOUtil()

    def __getattr__(self, name):
    	return getattr(self.instance, name)

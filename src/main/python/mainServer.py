#!/usr/bin/env python
import web
import time
import sys
import RPi.GPIO as GPIO
import json
from datetime import timedelta
from picamera import PiCamera
from time import sleep
from util.xmlConfigReader import *
from util.authentication import authenticate
import datetime

# Decorator methode for Header debugging
def getHeader():
	def wrapper(*args, **kwargs):
		txt = ""
		for k, v in web.ctx.env.items():
			txt += ": ".join([k, str(v)]) + "\n"
		print txt
		return f(*args, **kwargs)

	return wrapper



class ActionHelper:
	class ____ActionHelper:
		#delays for the signal, signallength etc..
		short_delay = 0.00015
		long_delay = 0.00045
		extended_delay = 0.0047
		#which pin on the pi and how many attempts
		NUM_ATTEMPTS = 10
		TRANSMIT_PIN = 23

		def transmit_code(self,code):
			'''Transmit a chosen code string using the GPIO transmitter'''
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self.TRANSMIT_PIN,GPIO.OUT)
			for t in range(self.NUM_ATTEMPTS):
				for i in code:
					if i == '1':
						GPIO.output(self.TRANSMIT_PIN, 1)
						time.sleep(self.short_delay)
						GPIO.output(self.TRANSMIT_PIN, 0)
						time.sleep(self.long_delay)
					elif i == '0':
						GPIO.output(self.TRANSMIT_PIN, 1)
						time.sleep(self.long_delay)
						GPIO.output(self.TRANSMIT_PIN, 0)
						time.sleep(self.short_delay)
					else:
						continue
				GPIO.output(self.TRANSMIT_PIN, 0)
				time.sleep(self.extended_delay)
			GPIO.cleanup()
			return None

		def takepicture(self,waitTime):
			filepath = None
			try:
				camera = PiCamera()
				camera.start_preview()
				sleep(int(waitTime))
				filepath = 'pic_' +  '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()) +'.jpg'
				camera.capture('./temp/' + filepath)
				camera.stop_preview()
				camera.close()
			except:
				filepath = None
				print "Cemera error"
				print "picture taken"
				print filepath
			return filepath

	instance = None
	def __init__(self):
		if not ActionHelper.instance:
			ActionHelper.instance = ActionHelper.____ActionHelper()
	def __getattr__(self, name):
		return getattr(self.instance, name)



class actuatorAction:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()
		self.actionHelperInst = ActionHelper()
	@authenticate
	def POST(self,actuatorId,actionName):
		output = '{"result":'
		aA = self.xmlHelperInst.getActuatorAction(actuatorId,actionName)
		if(aA is not None):
			print aA.get('function') , aA.get('parameter')
			try:
				print "get function and execute" + aA.get('function') + '  ' + aA.get('parameter');
				func = getattr(self.actionHelperInst,aA.get('function'))
				result = func(aA.get('parameter'))
				output +='"done"'
				if result != None:
					output += ',"return":"' + result + '"'
			except AttributeError:
					output +='"config error"'
		else:
			output +='"not defined"'
		output += '}'
		return output

class listActuator:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()

	@authenticate
	def POST(self):
		output = '{"actuator":['
		root = self.xmlHelperInst.getRoot()
		for child in root[0]:
					print 'child', child.tag, child.attrib
					output += str(child.attrib).replace("'",'"') + ','
		output += ']}'
		return output

class actuatorActionList:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()
	@authenticate
	def POST(self,actuatorId):
		output = '{"actions":['
		resActuator = self.xmlHelperInst.getActuator(actuatorId)
		if(resActuator is not None):
			for action in resActuator[0]: #List actions
							output += '"'+str(action.get('name')) + '",'
			output = output[:-1] + "]}" # remove last comma and close up
		return output

class serverInfo:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()
	@authenticate
	def POST(self):
		return json.dumps(self.xmlHelperInst.getServerInfo())

class serverUptime:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()
	@authenticate
	def POST(self):
		with open('/proc/uptime', 'r') as f:
			uptime_seconds = float(f.readline().split()[0])
			uptime_string = str(timedelta(seconds = uptime_seconds))
		return '{ "uptime":"'+uptime_string+'"}'

class resourceHandler:
	@authenticate
	def POST(self,filename):
		path = './temp/' + filename
		print path
		web.header('Content-type','images/jpeg')
		web.header('Content-transfer-encoding','binary')
		web.header('Content-Disposition', 'attachment; filename="' + filename + '"')
		imageBinary =  open(path, 'rb').read()
		return imageBinary

if __name__ == '__main__':
	urls = (
	'/server', 'serverInfo',
	'/server/getResource/(.*)', 'resourceHandler',
	'/server/uptime', 'serverUptime',
	'/actuator', 'listActuator',
	'/actuator/action/(.*)/(.*)', 'actuatorAction',
	'/actuator/actionList/(.*)', 'actuatorActionList'
	)
	app = web.application(urls, globals())
	print 'Start'
	app.run()

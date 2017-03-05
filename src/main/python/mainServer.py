#!/usr/bin/env python
import web
import time
import sys
import json
import logging
import logging.config

from util.xmlConfigReader import *
from util.authentication import authenticate
from util.serverUtil import serverUtil
from util.jsonRender import JsonRender
from util.gpioUtil import GPIOUtil
from util.cameraUtil import CameraUtil



# Decorator methode for Header debugging
def getHeader():
	def wrapper(*args, **kwargs):
		txt = ""
		for k, v in web.ctx.env.items():
			txt += ": ".join([k, str(v)]) + "\n"
		logging.debug( txt)
		return f(*args, **kwargs)

	return wrapper



class ActionHelper:
	class ____ActionHelper:
		TRANSMIT_PIN = 23
		def __init__(self):
			self.gpioUtil=GPIOUtil()
			self.cUtil=CameraUtil()

		def actionDummy(self,para1):
			return None

		def transmit_code(self,code):
			return self.gpioUtil.transmit_code(self.TRANSMIT_PIN,code)

		def takepicture(self,waitTime):
			return self.cUtil.takePicture(waitTime)

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
		output = None
		aA = self.xmlHelperInst.getActuatorAction(actuatorId,actionName)
		if(aA is not None):
			logging.debug( aA.get('function') + "-" + aA.get('parameter'))
			try:
				logging.debug( "get function and execute " + aA.get('function') + '  ' + aA.get('parameter'));
				func = getattr(self.actionHelperInst,aA.get('function'))
				result = func(aA.get('parameter'))
				if result != None:
					output = JsonRender.renderOK(str(result))
				else:
					output = JsonRender.renderOK("")
			except AttributeError, err:
					logging.debug(err)
					output = JsonRender.renderError("config error")
		else:
			#Action not found
			output = JsonRender.renderError("not defined")
		logging.debug(output)
		return output

class listActuator:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()

	@authenticate
	def POST(self):
		root = self.xmlHelperInst.getRoot()
		return JsonRender.renderActuatorList(root[0])

class actuatorActionList:
	def __init__(self):
		self.xmlHelperInst = XmlHelper()
	@authenticate
	def POST(self,actuatorId):
		#get Actuator
		resActuator = self.xmlHelperInst.getActuator(actuatorId)
		if(resActuator == None):
			return JsonRender.renderError("Actuator not found")
		return JsonRender.renderActionList(resActuator[0])

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
		sI = serverUtil()
		uptime_string = sI.getServerTime()
		return JsonRender.renderUptime(uptime_string)

class resourceHandler:
	@authenticate
	def POST(self,filename):
		path = './temp/' + filename
		logging.debug(path)
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
	logging.config.fileConfig("./config/logging.conf")
	app = web.application(urls, globals())
	logging.info("Start server")
	app.run()

	#Clean ups

	GPIOUtil().cleanUP()
	logging.info("Stop server")

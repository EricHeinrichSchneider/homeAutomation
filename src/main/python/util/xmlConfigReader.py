import xml.etree.ElementTree as ET
import logging
import types

class XmlHelper:
	instance = None
	configPath = './config/actuator.xml'

	class ____XmlHelper:
			def __init__(self,path):
				self.configPath = path
				self.root = None

			def loadConfig(self):
				if(self.root == None):
					logging.debug('parse config file')
					tree = ET.parse(self.configPath)
					self.root = tree.getroot()

			def getRoot(self):
				self.loadConfig()
				return self.root

			def getServerInfo(self):
				return self.getRoot().attrib

			def getActuator(self,actuatorId):
				logging.debug( 'child List')
				for child in self.getRoot()[0]:
							if(actuatorId == child.attrib.get('id')):
								logging.debug( 'found actuator'+ str(child))
								return child
				return None

			def getActuatorAction(self,actuatorId,actionName):
				resActuator = self.getActuator(actuatorId)
				if(resActuator is not None):
						for action in resActuator[0]: #List actions
							if(actionName == action.attrib.get('name')):
									logging.debug( 'found action'+ str(action))
									return action
				return None

	def __init__(self):
		if not XmlHelper.instance:
			XmlHelper.instance = XmlHelper.____XmlHelper(XmlHelper.configPath)

	def __getattr__(self, name):
		return getattr(self.instance, name)

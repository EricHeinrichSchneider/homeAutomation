import xml.etree.ElementTree as ET

class XmlHelper:
	instance = None

	class ____XmlHelper:
			def __init__(self):
				print 'parse config file'
				self.tree = ET.parse('./config/actuator.xml')
				self.root = self.tree.getroot()
				print 'parse config file - done'

			def getRoot(self):
				return self.root

			def getServerInfo(self):
				return self.root.attrib

			def getActuator(self,actuatorId):
				print 'child List'
				for child in self.root[0]:
							if(actuatorId == child.attrib.get('id')):
								print 'found actuator'+ str(child)
								return child
				return None

			def getActuatorAction(self,actuatorId,actionName):
				resActuator = self.getActuator(actuatorId)
				if(resActuator is not None):
						for action in resActuator[0]: #List actions
							if(actionName == action.attrib.get('name')):
									print 'found action'+ str(action)
									return action
				return None

	def __init__(self):
		if not XmlHelper.instance:
			XmlHelper.instance = XmlHelper.____XmlHelper()
	def __getattr__(self, name):
		return getattr(self.instance, name)

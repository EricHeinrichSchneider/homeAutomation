import web
import xml.etree.ElementTree as ET
import hashlib
import logging

# Decorator methode for the anotation authentication
def authenticate(f):
	def wrapper(*args, **kwargs):
		if(web.ctx.env.has_key("HTTP_AUTHENTICATE")):
			auth = web.ctx.env["HTTP_AUTHENTICATE"].split(" ")
			if(AuthenticationProvider().authenticate(auth[0],auth[1])):
				return f(*args, **kwargs)
		return '{"return":"authentication error"}'

	return wrapper



class AuthenticationProvider:
	class ____AuthenticationProvider:
		#delays for the signal, signallength etc..
		short_delay = 0.00015
		long_delay = 0.00045
		extended_delay = 0.0047
		#which pin on the pi and how many attempts
		NUM_ATTEMPTS = 10
		TRANSMIT_PIN = 23

		def __init__(self):
			# Load all users and there sectrects into a dic
			root = ET.parse('./config/login.xml').getroot()
			self.users ={}
			for child in root:
				self.users[child.attrib.get('name')] = hashlib.sha224(child.attrib.get('secret')).hexdigest()
				logging.debug( child.attrib.get('name') + "--" + self.users[child.attrib.get('name')])

		def authenticate(self,name,secret):
			if(self.users.has_key(name) and secret == self.users[name] ):
				return True
			return False

	instance = None
	def __init__(self):
		if not AuthenticationProvider.instance:
			AuthenticationProvider.instance = AuthenticationProvider.____AuthenticationProvider()
	def __getattr__(self, name):
		return getattr(self.instance, name)

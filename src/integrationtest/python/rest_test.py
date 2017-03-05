import requests
import json
import re
import hashlib

#Usning nosetests -v basic_test.py

# Test call basic rest api functionality
class TestUM:

	url="http://192.168.0.111:8080/"
	headers = {'AUTHENTICATE': 'eric.schneider '+hashlib.sha224(b"secretPhrase").hexdigest()}

	def test_actorOn(self):
		assert requests.post(self.url+'actuator/action/1/on', data={}, cookies={},headers=self.headers).text == '{"result":"ok","data":""}'

	def test_actorOff(self):
		assert requests.post(self.url+'actuator/action/1/off', data={}, cookies={},headers=self.headers).text == '{"result":"ok","data":""}'

	def test_actorActionList(self):
		assert requests.post(self.url+'actuator/actionList/2', data={}, cookies={},headers=self.headers).text == '{"actions":["on","off"]}'

	def test_actorList(self):
		result = '{"actuator":[{"type": "lamp", "id": "1", "name": "Lamp near the Desk"},{"type": "lamp", "id": "2", "name": "Lamp at the window left"},{"type": "lamp", "id": "3", "name": "Lamp at the window right"},{"type": "switch", "id": "4", "name": "Switch 1"},{"type": "switch", "id": "5", "name": "Switch 2"},{"type": "camera", "id": "6", "name": "Pi Camera"},]}'
		assert requests.post(self.url+'actuator', data={}, cookies={},headers=self.headers).text == result

	def test_actorNotexistAction(self):
		assert requests.post(self.url+'actuator/action/Lamp1NoGood/on', data={}, cookies={},headers=self.headers).text == '{"result":"error","message":"not defined"}'

	def test_serverInfo(self):
		assert requests.post(self.url+'server', data={}, cookies={},headers=self.headers).text == '{"latitude": "40.69694", "name": "The Dungeon", "longitude": "-73.9972"}'

	def test_serverUptime(self):
		# '002:21:47:00.490000' example string
		p = re.compile('^\d{3}:\d{2}:\d{2}:\d{2}.\d{6}$')
		response = requests.post(self.url+'server/uptime', data={},cookies={},headers=self.headers)
		print(response.text)
		o = json.loads(response.text)
		assert p.match(o.get("uptime")) != None

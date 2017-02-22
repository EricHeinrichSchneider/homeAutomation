import requests
import json
import re

# Test call basic rest api functionality 
class TestUM:

	url="http://192.168.0.107:8080/"

	def test_actorOn(self):
		assert requests.get(self.url+'actuator/action/Lamp1/on', data={}, cookies={}).text == '{"result":"done"}'        

	def test_actorOff(self):
		assert requests.get(self.url+'actuator/action/Lamp1/off', data={}, cookies={}).text == '{"result":"done"}'
		
	def test_actorActionList(self):
		assert requests.get(self.url+'actuator/actionList/Lamp2', data={}, cookies={}).text == 'actions:[on,off,]'
		
	def test_actorList(self):
		result = "actuator:[{'id': '1', 'name': 'Lamp1'},{'id': '2', 'name': 'Lamp2'},{'id': '3', 'name': 'Lamp3'},{'id': '4', 'name': 'Lamp4'},{'id': '5', 'name': 'Lamp5'},]"
		assert requests.get(self.url+'actuator', data={}, cookies={}).text == result
		
	def test_actorNotexitAction(self):
		assert requests.get(self.url+'actuator/action/Lamp1NoGood/on', data={}, cookies={}).text == '{"result":"not defined"}'
		
	def test_serverInfo(self):
		assert requests.get(self.url+'server', data={}, cookies={}).text == '{"latitude": "40.69694", "name": "The Dungeon", "longitude": "-73.9972"}' 
	
	def test_serverUptime(self):
		# '21:47:00.490000' example string
		p = re.compile('^\d{2}:\d{2}:\d{2}.\d{6}$')
		o = json.loads(requests.get(self.url+'server/uptime', data={}, cookies={}).text) 
		assert p.match(o.get("uptime")) != None 
		
		

		



'''
data= {
    'subject': 'Alice-subject',
    'addbbcode18': '%23444444',
    'addbbcode20': '0',
    'helpbox': 'Close all open bbCode tags',
    'message': 'alice-body',
    'poll_title': '',
    'add_poll_option_text': '',
    'poll_length': '',
    'mode': 'newtopic',
    'sid': '5b2e663a3d724cc873053e7ca0f59bd0',
    'f': '1',
    'post': 'Submit',
    }
 cookies = {'phpbb2mysql_data': 'a%3A2%3A%7Bs%3A11%3A%22autologinid%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22userid%22%3Bs%3A1%3A%223%22%3B%7D',
    'phpbb2mysql_t': 'a%3A9%3A%7Bi%3A3%3Bi%3A1330156986%3Bi%3A1%3Bi%3A1330160737%3Bi%3A5%3Bi%3A1330161702%3Bi%3A6%3Bi%3A1330179284%3Bi%3A2%3Bi%3A1330160743%3Bi%3A7%3Bi%3A1330163187%3Bi%3A8%3Bi%3A1330164442%3Bi%3A9%3Bi%3A1330164739%3Bi%3A10%3Bi%3A1330176335%3B%7D', 
    'phpbb2mysql_sid': '5b2e663a3d724cc873053e7ca0f59bd0',
    }
	
class TestUM:
 
    def setup(self):
        print ("TestUM:setup() before each test method")
 
    def teardown(self):
        print ("TestUM:teardown() after each test method")
 
    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
 
    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")
 
    def test_numbers_5_6(self):
        print 'test_numbers_5_6()  <============================ actual test code'
        assert multiply(5,6) == 30
 
    def test_strings_b_2(self):
        print 'test_strings_b_2()  <============================ actual test code'
        assert multiply('b',2) == 'bb'
'''
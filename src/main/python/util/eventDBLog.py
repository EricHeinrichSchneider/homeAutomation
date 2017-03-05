import sqlite3
import logging

class EventDBLog():
    instance = None

    class ____sensorDBLog:

        def __init__(self):
            self.conn = None

        def connect(self):
            connected = (self.conn == None) #if no connect object
            if(self.conn != None): # check connection when object exitsts
                    try:
                        resultset = conn.execute('''Select 'Hello in there'; ''')
                        connected = True
                    except sqlite3.ProgrammingError as e:
                        connected = False
            if(connected == False ): #if not try to connect
                self.conn = sqlite3.connect('./data/test.db', detect_types=sqlite3.PARSE_DECLTYPES)
                logging.debug("Opened database successfully")
                #check and if not there create table
                self.createTable()

        def createTable(self):
            self.conn.execute('''CREATE TABLE SENSOR_LOG IF NOT EXISTS
                               (
                               SENSOR_ID  CHAR(20) NOT NULL,
                               EVENT_TIME     TIMESTAMP  NOT NULL);''')

            self.conn.execute('''CREATE TABLE ACTION_LOG IF NOT EXISTS
                               (
                               ACTUATOR_ID    CHAR(20) NOT NULL,
                               ACTION         CHAR(20) NOT NULL,
                               RESULT         INT NOT NULL,
                               EVENT_TIME     TIMESTAMP  NOT NULL);''')

        def logSensorEvent(sensorID,timespamp):
            self.connect()
            c = self.conn.cursor()
            c.execute("INSERT INTO SENSOR_LOG values(?,?)", (sensorID,timespamp))
            self.conn.commit()

        def logActionEvent(actuatorIdsensorID,action,timespamp,result):
            self.connect()
            c = self.conn.cursor()
            c.execute("INSERT INTO ACTION_LOG values(?,?,?,?)", (actuatorIdsensorID,action,timespamp,result))
            self.conn.commit()

    def __init__(self):
    	if not sensorDBLog.instance:
    		sensorDBLog.instance = sensorDBLog.____XmlHelper()
    def __getattr__(self, name):
    	return getattr(self.instance, name)

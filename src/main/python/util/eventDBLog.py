import sqlite3
import logging

class EventDBLog():
    instance = None

    class ____EventDBLog:

        def __init__(self):
            self.conn = None

        def connect(self):
            connected = False
            if(self.conn != None): # check connection when object exitsts
                    try:
                        resultset = self.conn.execute('''Select 'Hello in there'; ''')
                        connected = True
                    except sqlite3.ProgrammingError as e:
                        connected = False

            if(connected == False ): #if not try to connect
                self.conn = sqlite3.connect('./data/test.db', detect_types=sqlite3.PARSE_DECLTYPES)
                logging.debug("Opened database successfully")
                #check and if not there create table
                self.createTable()

        def createTable(self):
            self.conn.executescript('''

                               CREATE TABLE IF NOT EXISTS SENSOR_LOG
                               (
                               SENSOR_ID  CHAR(20) NOT NULL,
                               EVENT_TIME     TIMESTAMP  NOT NULL);

                               CREATE TABLE IF NOT EXISTS ACTION_LOG
                               (
                               ACTUATOR_ID    CHAR(20) NOT NULL,
                               ACTION         CHAR(20) NOT NULL,
                               RESULT         INT NOT NULL,
                               EVENT_TIME     TIMESTAMP  NOT NULL);

                               ''')

        def logSensorEvent(self,sensorID,timespamp):
            self.connect()
            c = self.conn.cursor()
            c.execute("INSERT INTO SENSOR_LOG values(?,?)", (sensorID,timespamp))
            self.conn.commit()

        def logActionEvent(self,actuatorIdsensorID,action,timespamp,result):
            self.connect()
            c = self.conn.cursor()
            c.execute("INSERT INTO ACTION_LOG values(?,?,?,?)", (actuatorIdsensorID,action,timespamp,result))
            self.conn.commit()

        def getSensorLogToday(self):
            self.connect()
            cur = self.conn.cursor()
            cur.execute('''select SENSOR_ID,  EVENT_TIME
                           from SENSOR_LOG
                           WHERE EVENT_TIME BETWEEN DATE('now') AND DATE('now', '+1 day')
                           order by EVENT_TIME ''')
            return cur
            
        def closeConnection(self):
            if(self.conn != None):
                self.conn.close()

    def __init__(self):
    	if not EventDBLog.instance:
    		EventDBLog.instance = EventDBLog.____EventDBLog()
    def __getattr__(self, name):
    	return getattr(self.instance, name)

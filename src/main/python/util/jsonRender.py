import logging

class jsonRender:
    @staticmethod
    def renderActionList(actuator):
        output = '{"actions":['
        if(actuator is not None):
			for action in actuator: #List actions
							output += '"'+str(action.get('name')) + '",'
			output = output[:-1] # remove last comma
        return output + "]}"

    @staticmethod
    def renderUptime(uptime):
        return '{ "uptime":"'+uptime+'"}'

    @staticmethod
    def renderError(message):
        return '{"result":"error","message":"'+message+'"}'
    @staticmethod
    def renderOK(data):
        return '{"result":"ok","data":"'+data+'"}'

    @staticmethod
    def renderActuatorList(actuatorList):
        output = '{"actuator":['
        for child in actuatorList:
            logging.debug( 'child ' +  child.tag + ' - ' + str(child.attrib))
            output += str(child.attrib).replace("'",'"') + ','
        output += ']}'
        return output

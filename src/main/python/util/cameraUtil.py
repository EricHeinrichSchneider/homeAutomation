from picamera import PiCamera
from time import sleep
import datetime
import logging

class CameraUtil:
    instance = None
    tempPath = './temp/'

    class ____CameraUtil:

        def __init__(self,path):
            self.tempPath = path

        def takePicture(self,waitTime):
            filepath = None
            try:
            	camera = PiCamera()
            	camera.start_preview()
            	sleep(int(waitTime))
            	filepath = 'pic_' +  '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()) +'.jpg'
            	camera.capture(tempPath + filepath)
            	camera.stop_preview()
            	camera.close()
            except:
            	filepath = None
            	logging.error( "Camera error picture taken" +  filepath)
            return filepath


    def __init__(self):
    	if not CameraUtil.instance:
    		CameraUtil.instance = CameraUtil.____CameraUtil(CameraUtil.tempPath)

    def __getattr__(self, name):
    	return getattr(self.instance, name)

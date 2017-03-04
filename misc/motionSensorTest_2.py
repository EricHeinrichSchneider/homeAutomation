import RPi.GPIO as GPIO
import time

sensor = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

def my_callback(channel):
    print "falling edge detected on 17"

GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback, bouncetime=300)


while True:
    time.sleep(1)


import RPi.GPIO as GPIO

class Hardware():
    def __init__(self, profile):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18, GPIO.OUT)
        self.profile = profile

    def turn_fan_on(self):
        #if self.profile.fan_state == "off":
        GPIO.output(18, GPIO.HIGH)
        self.profile.fan_state = "on"

    def turn_fan_off(self):
        #if self.profile.fan_state == "on":
        GPIO.output(18, GPIO.LOW)
        self.profile.fan_state = "off"

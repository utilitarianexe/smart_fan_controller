from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
import time

ACTIVATION_THRESHOLD = 1.0

sensor = W1ThermSensor()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

base_temp = sensor.get_temperature() # in celcius                                                                                                                                                                    
led_on = False

def monitor_temp_loop(led_on, base_temp, sensor):
    while True:
        time.sleep(4)
        current_temp = sensor.get_temperature()
        print(current_temp, base_temp)
        if current_temp > base_temp + ACTIVATION_THRESHOLD and not led_on:
            print("turning led on")
            GPIO.output(18, GPIO.HIGH)
            led_on = True

        if current_temp < base_temp + ACTIVATION_THRESHOLD and led_on:
            print("turning led off")
            GPIO.output(18, GPIO.LOW)
            led_on = False

try:
    monitor_temp_loop(led_on, base_temp, sensor)
except KeyboardInterrupt:
    GPIO.output(18, GPIO.LOW)


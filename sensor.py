from w1thermsensor import W1ThermSensor

class Sensor():
    def __init__(self):
        self.sensor = W1ThermSensor()

    def get_inside_temp(self):
        temp_c = self.sensor.get_temperature()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

sensor = Sensor()

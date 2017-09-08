"""
Follow the instruction to setup.
I2C interface: https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/appendix-1-i2c-configuration-sensor-kit-v2-0-for-b-plus.html

Barometer BMP180
"""
import logging
import threading
import time
import Adafruit_BMP.BMP085 as BMP085

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    pins = {}

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin='i2c_77'):
        self.pins[pin] = True
        threading.Thread(target=self.get_data, args=(pin, )).start()

    def unplug(self, pin='i2c_77'):
        self.pins[pin] = False

    def get_data(self, pin):
        sensor = BMP085.BMP085()
        while self.pins[pin]:
            temp = sensor.read_temperature()
            pressure = sensor.read_pressure()
            alt = sensor.read_altitude()
            s_pressure = sensor.read_sealevel_pressure()

            self.send_response({
                'temperature': '{0:0.2f} C'.format(temp if not isinstance(temp, complex) else float('nan')),
                'pressure': '{0:0.2f} Pa'.format(pressure if not isinstance(pressure, complex) else float('nan')),
                'altitude': '{0:0.2f} m'.format(alt if not isinstance(alt, complex) else float('nan')),
                'sea_level_pressure': '{0:0.2f} Pa'.format(s_pressure if not isinstance(s_pressure, complex) else float('nan')),
            })
            time.sleep(1)

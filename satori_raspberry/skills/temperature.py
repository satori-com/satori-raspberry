"""
ds18b20 temperature sensor
"""

import os
import glob
import re
import time
import threading

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    device_dir = '/sys/bus/w1/devices/'
    pins = {}

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        os.system('dtoverlay w1-gpio gpiopin={} pullup=0'.format(pin))
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        self.pins[pin] = True
        t = threading.Thread(target=self.get_temperature, args = (pin, ))
        t.start()
    
    def unplug(self, pin):
        self.pins[pin] = False

    def get_temperature(self, pin):
        while self.pins[pin]:
            for folder in glob.glob(self.device_dir + '28*'):
                file = folder + '/w1_slave'
                with open(file, 'r') as content_file:
                    content = content_file.read()
                    temperature = re.findall("t=([0-9]+)", content, re.MULTILINE)
                    if temperature:
                        self.send_response({
                            't': float(temperature[0]) / 1000
                        })
            time.sleep(1)

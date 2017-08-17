"""
Humiture DHT11 sensor.
DHT11 has an integer precision only
"""

import threading
import time
import Adafruit_DHT

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    pins = {}

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        self.pins[pin] = True
        threading.Thread(target=self.get_data, args=(pin, )).start()

    def unplug(self, pin):
        self.pins[pin] = False

    def get_data(self, pin):
        while self.pins[pin]:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
            self.send_response({
                'temperature': '{0:0.1f}'.format(temperature),
                'humidity': '{0:0.1f}'.format(humidity)
            })
            time.sleep(1)

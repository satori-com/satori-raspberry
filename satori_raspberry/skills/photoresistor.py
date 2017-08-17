"""
Photoresistor sensor.
"""

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.add_event_detect(pin, self.GPIO.BOTH, callback=self.callback)
        resp = {
            "pin": pin,
            "action": "plugged"
        }
        self.send_response(resp)

    def unplug(self, pin):
        self.GPIO.remove_event_detect(pin)
        resp = {
            "pin": pin,
            "action": "unplugged"
        }
        self.send_response(resp)
    
    def callback(self, pin):
        resp = {
            "pin": pin,
            "light": self.GPIO.input(pin) ^ 1
        }
        self.send_response(resp)

"""
IR obstacle sensor.
"""

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.GPIO.add_event_detect(pin, self.GPIO.FALLING, callback=self.callback)
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
            "obstacle": "detected"
        }
        self.send_response(resp)

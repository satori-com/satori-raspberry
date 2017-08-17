"""
Button skill to get info when button is pressed.
API:
plug:
    Input: {
        "skill": "button",
        "action": "plug",
        "pin": 23,
    }
    Output: {
        "skill": "button",
        "response": {
            "button": "buttonPIN", // Example: button23
            "action": "pressed"
        }}

unplug:
    Input: {
        "skill": "button",
        "action": "unplug",
        "pin": 23,
    }
    Output: {
        "skill": "button",
        "response": {
            "button": "buttonPIN", // Example: button23
            "action": "unplugged"
        }}
"""

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def callback(self, pin):
        pressed = 1 if self.GPIO.input(pin) == 1 else 0
        resp = {
            "button": pin,
            "pressed": pressed
        }
        self.send_response(resp)

    def api_plug(self, message):
        if not self.check_field(message, 'pin', [i for i in range(1, 41)]):
            return False

        self.plug(message['pin'])
    
    def api_unplug(self, message):
        if not self.check_field(message, 'pin', [i for i in range(1, 41)]):
            return False

        self.unplug(message['pin'])

    def plug(self, pin):
        self.GPIO.setup(pin, self.GPIO.IN, pull_up_down = self.GPIO.PUD_UP)
        self.GPIO.add_event_detect(pin, self.GPIO.BOTH, callback=self.callback, bouncetime=50)
        resp = {
            "button": pin,
            "action": "plugged"
        }
        self.send_response(resp)
    
    def unplug(self, pin):
        self.GPIO.remove_event_detect(pin)
        resp = {
            "button": pin,
            "action": "unplugged"
        }
        self.send_response(resp)

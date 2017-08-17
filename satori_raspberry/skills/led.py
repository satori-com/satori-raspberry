"""
Control LEDs.
Set power on pins or remove the power from pins.
Be careful to use pins as a power supply for led. 
================================================
The 3.3V GPIO pins can supply a maximum of 50 mA
================================================

Use transistors to avoid burning pins 
"""

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def api_on(self, message):
        if not self.check_field(message, 'pin', [i for i in range(1, 41)]):
            return False

        self.on(message['pin'])
    
    def api_off(self, message):
        if not self.check_field(message, 'pin', [i for i in range(1, 41)]):
            return False

        self.on(message['pin'])

    def on(self, pin):
        self.GPIO.setup(pin, self.GPIO.OUT, initial=self.GPIO.LOW)
        self.GPIO.output(pin, 1)
        self.send_response({"pin": pin, "action": "on"})

    def off(self, pin):
        self.GPIO.setup(pin, self.GPIO.OUT, initial=self.GPIO.LOW)
        self.GPIO.output(pin, 0)
        self.send_response({"pin": pin, "action": "off"})
        
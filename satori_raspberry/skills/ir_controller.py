"""
Raspberry PI
IR Detector + IR controller
https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-23-ir-remote-control-sensor-kit-v2-0-for-b-plus.html

Covers NEC protocol
"""

from datetime import datetime
from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    start_time = 0
    val = 0
    prev_val = 0
    command = []

    NEC_PROTOCOL_INTERVAL = 562.5
    SENSIVITY = 20000

    hashes = {
        'FF6897': 'KEY_NUMERIC_0',
        'FF30CF': 'KEY_NUMERIC_1',
        'FF18E7': 'KEY_NUMERIC_2',
        'FF7A85': 'KEY_NUMERIC_3',
        'FF10EF': 'KEY_NUMERIC_4',
        'FF38C7': 'KEY_NUMERIC_5',
        'FF5AA5': 'KEY_NUMERIC_6',
        'FF42BD': 'KEY_NUMERIC_7',
        'FF4AB5': 'KEY_NUMERIC_8',
        'FF52AD': 'KEY_NUMERIC_9',
        'FF9867': 'KEY_REVERSE',
        'FFB04F': 'KEY_USD',
        'FFE01F': 'KEY_EQUAL',
        'FFA857': 'KEY_VOLUMEDOWN',
        'FF906F': 'KEY_VOLUMEUP',
        'FF22DD': 'KEY_PLAYPAUSE',
        'FF02FD': 'KEY_PREVIOUS',
        'FFC23D': 'KEY_NEXT',
        'FFA25D': 'KEY_POWER',
        'FF629D': 'KEY_MODE',
        'FFE21D': 'KEY_MUTE'
    }

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.GPIO.add_event_detect(pin, self.GPIO.FALLING, callback=self.get_signal)
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

    def get_signal(self, pin):
        if self.start_time == 0:
            self.val = self.GPIO.input(pin)

            if self.val != 0:
                return False

            self.start_time = datetime.now()
            while True:
                if self.val != self.prev_val:
                    now = datetime.now()
                    pulse_length = now - self.start_time
                    self.start_time = now
                    self.command.append((self.prev_val, pulse_length.microseconds))

                self.prev_val = self.val

                self.val = self.GPIO.input(pin)

                if self.val == 1:
                    now = datetime.now()
                    pulse_length = now - self.start_time
                    if pulse_length.microseconds / self.NEC_PROTOCOL_INTERVAL > 10:
                        break

            button = self.process_command(self.command)
            if button is not None:
                self.send_response({
                    'pin': pin,
                    'button': button
                })

            self.start_time = 0
            self.num_ones = 0
            self.prev_val = 0
            self.command = []

    def process_command(self, cmd):
        command = cmd[:] # make a copy of command
        bin_str = "".join(map(lambda x: "1" if x[1] > 1000 else "0", filter(lambda x: x[0] == 1, command)))

        if len(bin_str) >= 4:
            hash_code = "{0:0>4X}".format(int(bin_str, 2))
            if hash_code in self.hashes:
                return self.hashes[hash_code]
            else:
                print('[debg] Unknown button: {}'.format(hash_code))
        
        return None

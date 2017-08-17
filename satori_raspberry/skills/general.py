"""
General skill that can be used as base skill.
API:
cleanup:
    Input: {"skill": "general", "action": "cleanup"}
    Output: {"skill": "general", "response": "cleanup"}

ping:
    Input: {"skill": "general", "action": "ping"}
    Output: {"skill": "general", "response": "pong"}

setmode:
    Input: {
        "skill": "general",
        "action": "setmode",
        "mode": "BCM" // BCM or BOARD
    }

    Output: {"skill": "general", "response": "Mode has been changed to BOARD"}
    Output: {"skill": "general", "response": "Mode has been changed to BCM"}
    Output: {"skill": "general", "error": "mode is undefined"}
    Output: {"skill": "general", "error": "Use only BCM or BOARD as mode"}

setup:
    Input: {
        "skill": "general",
        "action": "setup",
        "pin": 23, // Pin number
        "mode": "IN", // IN or OUT
        "initial": "HIGH", // HIGH or LOW, requires for OUT mode
        "pud": "PUD_UP" // PUD_UP or PUD_DOWN, requires for IN mode
    }

    Output:
    {"skill": "general", "response": "Set mode OUT to pin 23. Initial: LOW; pull_up_down: PUD_DOWN"}
    {"skill": "general", "error": "X is undefined"} // pin, mode
    {"skill": "general", "error": "Use only X as Y"} // Example: use only [HIGH, LOW] as initial

output:
    Input: {
        "skill": "general",
        "action": "output",
        "pin": 23, // Pin number
        "output": 1 // Logical number 1 or 0 (+3.3V vs 0V)
    }

    Output:
       {"skill": "general", "response": "Output X to pin Y"} // Example: Output 1 to pin 23
       {"skill": "general", "error": "X is undefined"} // pin, output 

input:
    Input: {
        "skill": "general",
        "action": "input",
        "pin": 23 // Pin number
    }

    Output:
        {"skill": "general", "response": {"pin": "23", "value": 1}} // value: 1 or 0
        {"skill": "general", "error": "Use only X as pin"} // Example: use only [1,2,3....40] as pin
"""

from satori_raspberry.skills.base import Skill as BaseSkill

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def cleanup(self, message):
        self.GPIO.cleanup()
        self.send_response('cleanup')

    def ping(self, message):
        self.send_response('pong')

    def setmode(self, message):
        if not self.check_field(message, 'mode', ['BCM', 'BOARD']):
            return False

        mode = self.GPIO.BCM if 'BCM' == message['mode'] else self.GPIO.BOARD

        self.GPIO.setmode(mode)
        self.send_response("Mode has been changed to {}".format(message['mode']))

    def setup(self, message):
        if (not self.check_field(message, 'pin', [i for i in range(1, 41)]) or
            not self.check_field(message, 'mode', ['IN', 'OUT'])):
            return False

        pin = message['pin']
        mode = self.GPIO.OUT if message['mode'] == 'OUT' else self.GPIO.IN

        if mode == self.GPIO.OUT:
            if not self.check_field(message, 'initial', ['HIGH', 'LOW']):
                return False

            initial = self.GPIO.HIGH if message['initial'] == 'HIGH' else self.GPIO.LOW
            self.GPIO.setup(pin, mode, initial=initial)
            resp = 'Set mode {} to pin {}. Initial: {}'.format(message['mode'], pin, message['initial'])
        else:
            if not self.check_field(message, 'pull_up_down', ['PUD_UP', 'PUD_DOWN']):
                return False
            pull_up_down = self.GPIO.PUD_DOWN if message['initial'] == 'PUD_DOWN' else self.GPIO.PUD_UP
            self.GPIO.setup(pin, mode, pull_up_down=pull_up_down)
            resp = 'Set mode {} to pin {}. PUD: {}'.format(message['mode'], pin, message['pull_up_down'])

        self.send_response(resp)

    def output(self, message):
        if (not self.check_field(message, 'pin', [i for i in range(1, 41)]) or
            not self.check_field(message, 'value', [0, 1])
        ):
            return False

        pin = message['pin']
        value = message['value'] == 1
        self.GPIO.output(pin, value)
        resp = "Output {} to pin {}".format(message['value'], pin)
        self.send_response(resp)

    def input(self, message):
        if not self.check_field(message, 'pin', [i for i in range(1, 41)]):
            return False

        value = self.GPIO.input(message['pin'])
        resp = {'pin': message['pin'], 'value': value}
        self.send_response(resp)

    def check_field(self, message, field, values):
        if field not in message:
            self.send_error("'{}' is undefined".format(field))
            return False

        if field in message and message[field] not in values:
            self.send_error('Use only {} as {}'.format(values, field))
            return False

        return True

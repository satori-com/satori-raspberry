"""
Humiture DHT11 sensor
"""

import json
import Adafruit_DHT

class Skill(object):
    name = 'base'
    callbacks = []

    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel

    def plug(self, pin):
        pass
    
    def unplug(self, pin):
        pass

    def send_error(self, err):
        self.client.publish(self.channel, {"skill": self.name, "error": err})
        print('[debg] Skill [{}] Error: {}'.format(self.name, json.dumps(err)))
        for callback in self.callbacks:
            callback(self, err)

    def send_response(self, resp):
        self.client.publish(self.channel, {"skill": self.name, "response": resp})
        print('[debg] Skill [{}] Response: {}'.format(self.name, json.dumps(resp)))
        for callback in self.callbacks:
            callback(self, resp)

    def callback(self, callback):
        self.callbacks.append(callback)
    
    def check_field(self, message, field, values):
        if field not in message:
            self.send_error("'{}' is undefined".format(field))
            return False

        if field in message and message[field] not in values:
            self.send_error('Use only {} as {}'.format(values, field))
            return False

        return True
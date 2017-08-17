
class Skill(object):
    def __init__(self, gpio, client):
        self.gpio = gpio
        self.client = client

    def ping(self, message):
        print('pong')

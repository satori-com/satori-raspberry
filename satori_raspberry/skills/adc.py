"""
ADC controller.
ADC has 4 Analog inputs. To read such inputs use their indexes:
A0 = 0
A1 = 1
A2 = 2
A3 = 3

Example:
Read Analog pin 0:
adc = controller.skill('adc')
adc.read(0) # value from 0-255
"""
import smbus

from satori_raspberry.skills.base import Skill as BaseSkill

bus = smbus.SMBus(1)

class Skill(BaseSkill):
    def __init__(self, gpio, client, channel):
        self.GPIO = gpio
        self.client = client
        self.channel = channel
        self.address = 0x48 # default joystick address

    def set_address(self, address):
        self.address = address

    def read(self, ch):
        try:
            if ch == 0:
                bus.write_byte(self.address, 0x40)
            if ch == 1:
                bus.write_byte(self.address, 0x41)
            if ch == 2:
                bus.write_byte(self.address, 0x42)
            if ch == 3:
                bus.write_byte(self.address, 0x43)
            bus.read_byte(self.address) # dummy read to start conversion
        except Exception as e:
            print("Address: {}".format(self.address))
            print(e)
        return bus.read_byte(self.address)

    def write(self, val):
        try:
            temp = val # move string value to temp
            temp = int(temp) # change string to integer
            # print temp to see on terminal else comment out
            bus.write_byte_data(self.address, 0x40, temp)
        except Exception as e:
            print("Error: Device address: {}".format(self.address))
            print(e)

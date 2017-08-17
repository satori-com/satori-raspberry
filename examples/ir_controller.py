"""
https://www.sunfounder.com/infrared-receiver-module.html

Ciruit schema
Infrared-receiver module | Raspberry Pins
===========================================
           S             | GPIO6
           -             | GND
           +             | 3.3V
===========================================
"""

import os, time

from satori_raspberry.controller import Controller

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def buttons(skill, response):
    actions = {
        'KEY_POWER': 'I think we need to turn off the TV',
        'KEY_VOLUMEUP': 'Let\'s make a little louder',
        'KEY_VOLUMEDOWN': 'Let\'s make a little quiter',
        'KEY_NUMERIC_0': 'Oh, Channel 0',
        'KEY_NUMERIC_1': 'Okay, channel 1',
        'KEY_NUMERIC_2': 'Boring',
        'KEY_NUMERIC_3': 'Still boring',
        'KEY_NUMERIC_4': 'Something new',
        'KEY_NUMERIC_5': '5th channel!',
        'KEY_NUMERIC_6': 'You pressed 6, isn\'t it?',
        'KEY_NUMERIC_7': 'Made it!',
        'KEY_NUMERIC_8': 'Press POWER, please',
        'KEY_NUMERIC_9': {"code": "O*HF&*($)@", "action": "secret"}
    }
    if 'button' in response and response['button'] in actions:
        # Here you can do anything you want! React on buttons and publish any text to Satori
        # or do any other actions
        skill.client.publish(skill.channel, actions[response['button']])

def main():
    ctrl = Controller(ROOT_DIR + '/config.json')
    ctrl.connect()
    ir = ctrl.skill('ir_controller')
    ir.plug(6)
    ir.callback(buttons)

    ctrl.wait_messages()

if __name__ == "__main__":
    main()

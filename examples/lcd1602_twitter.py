"""
Follow the instruction to setup.
I2C interface: https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/appendix-1-i2c-configuration-sensor-kit-v2-0-for-b-plus.html

Do not forget to install `python3-smbus` package
Plug LCD screen to SDA and SDL pins
"""

import os
import time
from queue import Queue
from satori.rtm.client import make_client, SubscriptionMode

from satori_raspberry.controller import Controller

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    ctrl = Controller(ROOT_DIR + '/config.json')
    ctrl.connect()

    # Run in console i2cdetect -y 1 to get the address.
    # Example output:
    # pi@raspberrypi:~ $ i2cdetect -y 1
    #  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    # 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    # 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
    # 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 70: -- -- -- -- -- -- -- --
    #
    # Address should be 0xXX where XX is digital number.
    # Example: 0x27
    lcd = ctrl.skill('lcd').plug(0x27)
    # Get credentials on this page: https://www.satori.com/channels/Twitter-statuses-sample
    fifo = Queue(10)
    
    with make_client('ENDPOINT', 'APP_KEY') as client:
        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for message in data['messages']:
                    if not fifo.full() and message['text'] is not None and len(message['text']) <= 32:
                        fifo.put_nowait(message['text'])

        observer = SubscriptionObserver()
        client.subscribe('Twitter-statuses-sample', SubscriptionMode.SIMPLE, observer,
            args={'filter': 'select * from `Twitter-statuses-sample` where lang="en"'})

        while True:
            message = fifo.get()
            lcd.message(message, 2)
            time.sleep(1)
            lcd.clear()

        ctrl.wait_messages()



if __name__ == "__main__":
    main()

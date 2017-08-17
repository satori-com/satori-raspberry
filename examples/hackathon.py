"""
Follow the instruction to setup.
I2C interface: https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/appendix-1-i2c-configuration-sensor-kit-v2-0-for-b-plus.html

Do not forget to install `python3-smbus` package
Plug LCD screen to SDA and SDL pins
"""

import os
import time
import threading

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

    lcd_address = 0x27
    dht11_pin = 26 #GPIO 26
    touch_sensor_pin = 16 #GPIO 16
    
    lcd = ctrl.skill('lcd').plug(lcd_address)
    dht11 = ctrl.skill('humiture')
    dht11.plug(dht11_pin)

    button = ctrl.skill('button')
    button.plug(touch_sensor_pin)

    barometer = ctrl.skill('barometer')
    barometer.plug('sda')

    try:
        # Connect Joystick
        t = threading.Thread(target=get_coords, args=(ctrl,))
        t.start()

        # Credentials from https://www.satori.com/channels/Twitter-statuses-sample
        with make_client('wss://open-data.api.satori.com', 'dae05AEf68aF3AeC366Be8F2855e4c4f') as client:
            fifo = Queue(10)
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
    except KeyboardInterrupt:
        print('Bye bye!')
        os._exit(0)

def get_coords(ctrl):
    adc = ctrl.skill('adc')
    x_in = 0 # A0
    y_in = 1 # A1
    prev_x = 0
    prev_y = 0

    while True:
        x = adc.read(x_in)
        y = adc.read(y_in)

        if x != prev_x or y != prev_y:
            prev_x = x
            prev_y = y
            adc.send_response({'x': x, 'y': y})
        time.sleep(0.05)

if __name__ == "__main__":
    main()

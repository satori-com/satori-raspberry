import os

from satori_raspberry.controller import Controller

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    dht11_pin = 23
    ctrl = Controller(ROOT_DIR + '/config.json')
    ctrl.connect()
    ctrl.skill('humiture').plug(dht11_pin)
    ctrl.wait_messages()

if __name__ == "__main__":
    main()

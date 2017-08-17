import os

from satori_raspberry.controller import Controller

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    led1 = 23
    led2 = 24
    ctrl = Controller(ROOT_DIR + '/config.json')
    ctrl.connect()
    ctrl.skill('led').on(led1)
    ctrl.skill('led').on(led2)
    ctrl.wait_messages()

if __name__ == "__main__":
    main()

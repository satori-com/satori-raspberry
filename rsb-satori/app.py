import os

from satori_raspberry.controller import App

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    app = App(ROOT_DIR + '/config.json')
    app.run()

if __name__ == "__main__":
    main()

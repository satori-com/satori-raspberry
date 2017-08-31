Raspberry PI skill manager
==============================

Skill manager framework uses to fast prototyping of boards controlled by RaspberryPi

Requirements
------------------------------

  - Installed **python3** and **pip3**
  - Python3 devel package:  
    `sudo apt-get install python3-dev`  
      or  
    `sudo yum install python-devel`
  - libow-dev to work with 1-wire sensors, like DHT11 or Temperature:  
    `sudo apt-get install libow-dev`
  - python3-smbus package:
    `sudo apt-get install python3-smbus`


Installation
------------------------------
Clone the repo:
```
git clone ssh://git@bitbucket.addsrv.com/~azinoviev/raspberry.git
cd raspberry
pip3 install -r requirements.txt
```

or you can use pip (use `process-dependency-links` flag to install dependencies):
```
pip3 install satori-raspberry --process-dependency-links
```

**ATTENTION: The framework uses GPIO library that can be compiled only in Raspberry Pi**

There are a lot of examples of how to work with different sensors and modules.
Moreover you can use GPIO directly in your program or use any additional libraries!

At this moment framework supports the following sensors and modules:
  - ds18b20 temperature sensor
  - barometer (BMP180)
  - Photoresistor
  - Any LEDs
  - LCD: Sunfounder LCD1602 screen
  - IR obstacle detector
  - IR Controller: https://www.sunfounder.com/media-remote-control-with-ir-receiver-module-for-raspberry-pi.html
  - Humiture DHT11 sensor
  - Buttons
  - Joystick
  - ADC controller

Run the Example
-------------------------------
You need to create a config.json file with your Satori credentials first.
And then - run any example
```
cp examples/config.example.json examples/config.json
nano examples/config.json
PYTHONPATH=. python3 examples/hackathon.py
```

or if you installed package via pip
```
cd examples
cp config.example.json config.json
nano config.json
python3 hackathon.py
```

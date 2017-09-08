#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'RPi.GPIO==0.6.3',
    'satori-rtm-sdk==1.3.0',
    'Adafruit_DHT>=1.3.2',
    'smbus2==0.2.0'
]

dependencies = [
    'git+https://github.com/adafruit/Adafruit_Python_DHT#egg=Adafruit_DHT-1.3.2',
    'git+https://github.com/adafruit/Adafruit_Python_GPIO.git#egg=Adafruit_GPIO-1.0.3',
    'git+https://github.com/adafruit/Adafruit_Python_BMP.git#egg=Adafruit_BMP-1.5.2'
]

long_description = '''
Requirements
------------------------------

  - Installed **python3** and **pip3**
  - Python3 devel package::

      sudo apt-get install python3-dev

    or::

      sudo yum install python-devel

  - `libow-dev` to work with 1-wire sensors, like DHT11 or Temperature::

      sudo apt-get install libow-dev

  - `python3-smbus` package::

      sudo apt-get install python3-smbus

Installation
------------------------------

The latest Adafruit sensors library is located on GitHub: https://github.com/adafruit/Adafruit_Python_DHT

In order to install this library we use `dependency_links`. So use `--process-dependency-links` flag when installing the satori-raspberry module::

  pip3 install satori-raspberry --process-dependency-links

**ATTENTION: The satori-raspberry framework uses GPIO library that can be compiled only in Raspberry Pi**
'''

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ]

setup(
    name='satori-raspberry',
    version='0.0.3',
    description='Raspberry Pi framework to work with Satori',
    long_description=long_description,
    author='Satori Worldwide, Inc.',
    author_email='sdk@satori.com',
    url='https://github.com/satori-com/satori-raspberry',
    packages=find_packages(exclude=['examples']),
    install_requires=requires,
    dependency_links=dependencies,
    classifiers=classifiers,
    license='Proprietary',
    keywords=['satori', 'raspberry', 'iot'],
    zip_safe=True)

#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'RPi.GPIO==0.6.3',
    'satori-rtm-sdk==1.3.0',
    'Adafruit_DHT>=1.3.2',
    'smbus2==0.2.0'
]

dependencies = [
    'git+https://github.com/adafruit/Adafruit_Python_DHT#egg=Adafruit_DHT-1.3.2'
]

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
    version='0.0.2',
    description='Raspberry Pi framework to work with Satori',
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

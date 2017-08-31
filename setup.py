#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as r:
    lines = [line for line in r.read().splitlines() if line.strip() != '']
    reqs = [req for req in lines if not req.startswith('git+')]
    deps = [dep for dep in lines if dep.startswith('git+')]

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
    version='0.0.1',
    description='Raspberry Pi framework to work with Satori',
    author='Satori Worldwide, Inc.',
    author_email='sdk@satori.com',
    url='https://github.com/satori-com/satori-raspberry',
    packages=find_packages(exclude=['examples']),
    install_requires=reqs,
    dependency_links=deps,
    classifiers=classifiers,
    license='Proprietary',
    keywords=['satori', 'raspberry', 'iot'],
    zip_safe=True)

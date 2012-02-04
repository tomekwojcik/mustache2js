#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='mustache2js',
    version='1.0.1',
    scripts=[
        'mustache2js.py'
    ],
    entry_points={
        'console_scripts': [
            'mustache2js=mustache2js:main'
        ]
    },
    zip_safe=False,
    author=u'Tomek Wójcik',
    author_email='labs@tomekwojcik.pl',
    description='Awesome Mustache to JavaScript converter',
    license='MIT',
    url='https://github.com/tomekwojcik/mustache2js'
)
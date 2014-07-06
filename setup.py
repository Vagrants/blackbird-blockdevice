#!/usr/bin/env python
# -*- encodig: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='blackbird-blockdevice',
    version='0.1.0',
    description=(
        'Low level discovery of block devices.'
    ),
    author='ARASHI, Jumpei',
    author_email='jumpei.arashi@arashike.com',
    url='https://github.com/Vagrants/blackbird-blockdevice',
)

#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pytrack',
      version='1.0',
      description='Track File Changes',
      author='Dalibor Menkovic',
      author_email='dalibor.menkovic@gmail.com',
      url='https://github.com/dalibor91/pytracker',
      packages=['pytrack'],
      scripts=['bin/pytrack'],
)
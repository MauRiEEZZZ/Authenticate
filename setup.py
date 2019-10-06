#!/usr/bin/env python

from distutils.core import setup

setup(
   name='Helpers',
   version='0.1.6',
   description='this module will help you authenticate to azure resources used in your python script',
   author='Maurice de Jong',
   author_email='maurice@deholanda.com',
   packages=['Helpers'],  #same as name
   install_requires=['adal', 'azure'], #external packages as dependencies
)
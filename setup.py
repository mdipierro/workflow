#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

setup(name='file-workflow',
      version='0.1',
      description='a minimalist file-based workflow system',
      author='Massimo DiPierro',
      author_email='massimo.dipierro@gmail.com',
      long_description=open("README.md").read(),
      url='https://github.com/mdipierro/workflow',
      install_requires=[],
      py_modules=["workflow"],
      license= 'BSD',
      keywords='workflow',
     )

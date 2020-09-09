#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup

setup(
    name="ipautil",
    version="0.0.1",
    description="decode, resign, etc",
    author="Taichi Kotake",
    packages=['ipautil'],
    entry_points={
        'console_scripts': [
            'ipautil = ipautil.cli:main',
        ],
    },
    install_requires=[
        'colorama',
    ],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

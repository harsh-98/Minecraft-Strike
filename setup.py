# -*- coding: utf-8 -*-

"""
Minecraft Strike
"""

from __future__ import print_function
import sys
if sys.version_info[0] >= 3:
    print("Sorry, minecraft_strike needs python <= 2.7", file=sys.stderr)
    sys.exit(-1)

from setuptools import setup, find_packages

REQUIREMENTS = [
    "pyglet==1.3.1",
]


NAME = "Minecraft-Strike"
DESCRIPTION = "Multiplayer Minecraft in Python"
VERSION = "1.0"

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      packages=find_packages(),
      entry_points={
          "console_scripts": ["mstrike = minecraft_strike.arg_handler:main"]
      },
      classifiers=[
          "Intended Audience :: End Users/Desktop",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
      ],
      install_requires=REQUIREMENTS,)

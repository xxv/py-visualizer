#!/usr/bin/env python

"""Example of using this animation library with MQTT.

This uses paho-mqtt. To install, do:

    pipenv install paho-mqtt

or

    pip install paho-mqtt

and then do:

    cp mqtt_config.json.example mqtt_config.json

and edit mqtt_config.json with your MQTT configuration.
"""

from __future__ import print_function
import sys

from mqtt_source import MQTTSource
from anim import Animator
from patterns import DebugPattern


def main():
    if len(sys.argv) != 2:
        print("Usage: {} MQTT_CONFIG_FILE".format(sys.argv[0]))
        sys.exit(1)

    config_file = sys.argv[1]
    source = MQTTSource(config_file)
    source.connect()
    anim = Animator(source, DebugPattern())
    anim.loop_forever()


if __name__ == '__main__':
    main()

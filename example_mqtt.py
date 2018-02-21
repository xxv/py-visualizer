#!/usr/bin/env python

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

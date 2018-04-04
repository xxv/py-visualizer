"""Visualization patterns"""

from __future__ import print_function
from anim import Pattern


class DebugPattern(Pattern):
    """A handy pattern that just prints out events"""
    _event = None

    def draw(self):
        if self._event:
            print("Event: {}".format(self._event))
            self._event = None

    def on_event(self, event):
        self._event = event

    def stop(self):
        print("Stopped the pattern.")

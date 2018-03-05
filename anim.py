"""Components for making simple event-driven visualization animations"""

import queue
from threading import Thread
import time


class Pattern(object):
    """A visualization pattern"""
    def tick(self):
        """Call this on a regular basis to update any animation state"""
        pass

    def on_event(self, event):
        """Call this to add a new event to the visualization"""
        pass


class Source(object):
    """An event source

    Implement loop() and call trigger() when you have an event"""
    def __init__(self):
        self._listener = None
        self._keepon = True

    def trigger(self, event):
        """Trigger an event"""
        if self._listener:
            self._listener(event)

    def set_listener(self, listener):
        """Set the event listener

        listener takes one user-defined argument, event"""
        self._listener = listener

    def loop(self):
        """Processing-style loop() method

        This will be called until the source is told to stop.
        Alternatively, you can override loop_forever() if desired."""
        # By default, just terminate the loop so there's not a freewheeling
        # loop running on a thread.
        self._keepon = False

    def loop_forever(self):
        """Main source event loop"""
        while self._keepon:
            self.loop()

    def stop(self):
        """Stop the default event loop"""
        self._keepon = False


class TestSource(Source):
    def loop(self):
        print("Test source triggering...")
        self.trigger(None)
        time.sleep(1)

    def stop(self):
        print("Test source stopping...")
        Source.stop(self)


class Animator(object):
    """Animates events from the source using the pattern

    This queues events and runs the source loop on a background
    thread so the animation is smooth."""

    _event_queue = queue.Queue()
    _keepon = True
    _thread = None
    DELAY_MS = 8  # 120 ticks per minute

    def __init__(self, source, pattern):
        self._source = source
        self._pattern = pattern
        source.set_listener(self._enqueue_event)

    def _enqueue_event(self, event):
        self._event_queue.put(event)

    def _process_queue(self):
        try:
            while True:
                self._pattern.on_event(self._event_queue.get(block=False))
        except queue.Empty:
            pass

    def stop(self):
        """Stop the animation"""
        self._keepon = False
        print("Animation stopped. Stopping source...")
        self._source.stop()
        if self._thread:
            self._thread.join()
        print("Done.")

    def loop_forever(self):
        """Main animation loop

        Call this from your script. Waits 1ms between ticks."""
        self._thread = Thread(target=self._source.loop_forever)
        self._thread.start()
        print("Animation started.")
        try:
            while self._keepon:
                self._process_queue()
                self._pattern.tick()
                time.sleep(self.DELAY_MS/1000)
        except KeyboardInterrupt:
            self.stop()

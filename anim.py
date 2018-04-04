"""Components for making simple event-driven visualization animations"""

from __future__ import division, print_function
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty
from threading import Thread
import time


class Pattern(object):
    """A visualization pattern."""

    def draw(self):
        """Called by Animator on regular basis to update any animation state.

        This is usually where you put the code that draws the state of your
        animation pattern.
        """
        pass

    def on_event(self, event):
        """Called when a Source triggers an event.

        This is usually where you update your Pattern's animation state
        to then later be drawn by draw().
        """
        pass

    def stop(self):
        """Called when the animation terminates."""
        pass


class Source(object):
    """A source of events.

    Implement loop() and call trigger() when you have an event.
    loop() will be called on its own thread and trigger() passes events
    to a Queue so most threading concerns should be handled automatically
    on the consumer end.
    """
    def __init__(self):
        self._listener = None
        self._keepon = True

    def trigger(self, event):
        """Trigger an event"""
        if self._listener:
            self._listener(event)

    def set_listener(self, listener):
        """Set the event listener

        listener takes one user-defined argument, event.
        """
        self._listener = listener

    def loop(self):
        """Processing-style loop() method.

        This will be called until the source is told to stop.
        Alternatively, you can override loop_forever() if your Source
        has its own event loop.
        """
        # By default, just terminate the loop so there's not a freewheeling
        # loop running on a thread.
        self._keepon = False

    def loop_forever(self):
        """Main source event loop."""
        while self._keepon:
            self.loop()

    def stop(self):
        """Stop the default event loop"""
        self._keepon = False


class TestSource(Source):
    """A simple test source."""
    def loop(self):
        print("Test source triggering...")
        self.trigger(None)
        time.sleep(1)

    def stop(self):
        print("Test source stopping...")
        Source.stop(self)


class Animator(object):
    """Animate events coming from the Source using the Pattern.

    This queues events and runs the Source loop on a background
    thread so the animation is smooth.
    """

    _event_queue = Queue()
    _keepon = True
    _thread = None

    def __init__(self, source, pattern, frames_per_second=120):
        """Animator

        Keyword arguments:
        frames_per_second -- the frequency that Pattern's draw() gets called
        """
        self._source = source
        self._pattern = pattern
        assert frames_per_second > 0, "frames_per_second must be > 0"
        self._delay_s = 1/frames_per_second
        source.set_listener(self._enqueue_event)

    def _enqueue_event(self, event):
        self._event_queue.put(event)

    def _process_queue(self):
        try:
            for _ in range(100):  # ensure draw() doesn't get blocked
                self._pattern.on_event(self._event_queue.get(block=False))
        except Empty:
            pass

    def stop(self):
        """Stop the animation."""

        self._keepon = False
        self._pattern.stop()
        print("Animation stopped. Stopping source...")
        self._source.stop()
        if self._thread:
            self._thread.join()
        print("Done.")

    def loop_forever(self):
        """Main animation loop.

        This will block until a keyboard interrupt is sent.
        """
        self._thread = Thread(target=self._source.loop_forever)
        self._thread.start()
        print("Animation started.")
        try:
            while self._keepon:
                self._process_queue()
                self._pattern.draw()
                time.sleep(self._delay_s)
        except KeyboardInterrupt:
            self.stop()

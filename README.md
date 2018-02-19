A simple event-driven animation framework
=========================================

This lightweight framework makes it easy to make animation patterns and
visualizations that are driven by triggered events.

Animations are broken up into two main components: Sources and Patterns.

Source
------

A source of events.

This can be anything from a random-number generator to network requests that
fetch real-time data. Sources have independent loops from your animation loops,
so you can feel free to do operations here that take a long time and your
animation will keep running smoothly.

```
import time

class TickSource(Source):
    # this method will be called repeatedly until the animation is shut down
    def loop(self):
	# trigger an event once per second
        self.trigger({})
        time.sleep(1)
```

Pattern
-------

Your animation/visualization pattern.

This is your main animation loop. Here, you draw animations and handle incoming
events. Events are delivered to you on the same thread as your animation pattern,
so you don't need to worry about multi-threading issues.

```
class MyPattern(Pattern):
    def on_event(self, event):
	print("Got event {}".format(event))

    def tick(self):
        print('.', end='', flush=True)
```

Animator
--------

The glue that connects your Source to your Pattern.

Putting it all together
-----------------------

```
def main():
    anim = Animator(TickSource(), MyPattern())
    anim.loop_forever()

if __name__ == '__main__':
    main()
```

This will run forever until it gets a keyboard interrupt and then shut things
down cleanly.

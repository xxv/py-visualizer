import random
import time

from anim import Animator, Pattern, Source

class MyPattern(Pattern):
    _count = 0
    _symbol = '.'
    _frame = 0

    def on_event(self, event):
        # just store the event's data locally to be used by tick()
        # Generally one doesn't output anything here.
        self._count = event['count']
        self._symbol = event['symbol']

    def tick(self):
        # this is where we draw our display
        self._frame += 1

        if self._count:
            symbol = self._symbol
        else:
            symbol = '_-¯-'[self._frame % 4]

        self._count = max(0, self._count - 1)

        print(symbol, end='', flush=True)

class RandomSource(Source):
    rand = random.Random()

    def loop(self):
        # pick a random number of one of the symbols below
        count = random.randint(1, 10)
        symbol = random.choice(('o', 'x', '#', '@', '*'))
        event = {
                'count': count,
                'symbol': symbol
                }
        self.trigger(event)
        # then wait a litle bit to trigger another event
        time.sleep(random.uniform(0.5, 1.5))

def main():
    source = RandomSource()
    pattern = MyPattern()
    anim = Animator(source, pattern)

    anim.loop_forever()

if __name__ == '__main__':
    main()

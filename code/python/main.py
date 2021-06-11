import signal

from models import WordClock
from settings import birthdays, display_cls, words


if __name__ == '__main__':
    # Setup clock and display
    wordclock = WordClock(display_cls, words, birthdays)
    signal.signal(signal.SIGTERM, wordclock.cleanup)

    while True:
        cleanup = False
        exception = None
        try:
            wordclock.tick()
        except Exception:
            wordclock.cleanup(exit=False)
            raise

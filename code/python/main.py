from functools import partial
import signal
import sys

from models import WordClock
from settings import birthdays, display_cls, words


def cleanup(cleanup_fn, *args):
    """
    Cleanup function. Signal handlers take are passed in two args by default, hence the unused *args.

    Args:
        cleanup_fn (function): cleanup function to run
    """
    cleanup_fn()
    sys.exit(0)


if __name__ == '__main__':
    # Setup clock and display
    wordclock = WordClock(display_cls, words, birthdays)
    signal.signal(signal.SIGTERM, partial(cleanup, wordclock.cleanup))

    while True:
        exception = None
        try:
            wordclock.tick()
        except Exception:
            wordclock.cleanup()
            raise

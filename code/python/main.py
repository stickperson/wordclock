import signal
import sys
from functools import partial

from animations import ColorCycle, Pulse, Rainbow
from buttons import ButtonStateManager, MockButton
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


def when_held(animations, button):
    current_state = button.current_state
    if current_state:
        action = animations[current_state - 1]
        # Some animations will only be run if the button is currently pressed down. If it should be run after
        # release until the button is pressed, add `continue_after_button_pressed = True` to the animation
        # instance
        if button.is_held or getattr(action, 'continue_after_button_pressed', False):
            action.animate()


def add_buttons(clock):
    pulse = Pulse(clock, clock.displayer.pixels, speed=0.05, period=3)
    pulse.run_alone = False
    color_cycle = ColorCycle(clock, clock.displayer.pixels, speed=0.05)
    rainbow = Rainbow(
        clock, clock.displayer.pixels, speed=0.1, words=[clock.words['ALL']])

    button_animations = [pulse, color_cycle, rainbow]
    button_manager = ButtonStateManager(
        len(button_animations), on_reset=clock.reset
    )
    button = MockButton(
        4,
        button_manager,
        hold_time=0.5,
        tick_fn=partial(when_held, button_animations)
    )
    clock.add_button(button)


if __name__ == '__main__':
    # Setup clock and display
    wordclock = WordClock(display_cls, words, birthdays)
    add_buttons(wordclock)
    signal.signal(signal.SIGTERM, partial(cleanup, wordclock.cleanup))

    while True:
        exception = None
        try:
            wordclock.tick()
        except Exception:
            wordclock.cleanup()
            raise

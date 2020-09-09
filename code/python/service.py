import datetime
from functools import partial
import sys

from animations import ColorCycler, Dim, Rainbow, TheaterChase
from models import Clock, Timer
from settings import birthdays, display_cls, words
from button_managers import MockButtonHandler


def display_birthday(now, animation, birthdays, button, **kwargs):
    if button.current_state:
        return
    month = now.month
    day = now.day
    for birthday in birthdays:
        if birthday.month == month and birthday.day == day:
            animation.update()
            return


def update_clock(now, clock, **kwargs):
    clock.update(now.hour, now.minute)


def reset_display_and_clock(clock, displayer, **kwargs):
    displayer.reset()
    now = datetime.datetime.now()
    clock.update(now.hour, now.minute)


def run_animation(animation, animations, button, **kwargs):
    current_state = button.current_state
    if current_state:
        button_animation = animations[button.current_state - 1]
        if button_animation != animation:
            return
        if button.is_pressed or getattr(animation, 'continue_after_button_pressed', False):
            animation.update()


if __name__ == '__main__':
    # Setup clock and display
    displayer = display_cls(rows=10, columns=13, max_brightness=25)
    clock = Clock(displayer=displayer, color=None, words=words)

    # Update the clock immediately
    now = datetime.datetime.now()
    clock.update(now.hour, now.minute)

    # Birthday handler
    birthday_animation = Rainbow(displayer, words=[words['HAPPY'], words['BIRTHDAY']])

    # Define animations. These will be cycled through when clicking the button.
    color_cycler = ColorCycler(clock, displayer)
    dim = Dim(clock, displayer)
    button_rainbow = Rainbow(displayer, words=[words['ALL']])
    button_chase = TheaterChase(displayer, words['ALL'])

    # These two animations should continue even after the button is released. This might be a hack but it doesn't
    # really make sense for the animation itself to care.
    button_rainbow.continue_after_button_pressed = True
    button_chase.continue_after_button_pressed = True

    button_animations = [color_cycler, dim, button_rainbow, button_chase]
    button = MockButtonHandler(
        states=len(button_animations), on_reset=partial(reset_display_and_clock, clock, displayer)
    )

    # All timers. Change time to speed up/slow down animations.
    birthday_timer = Timer(50, display_birthday, animation=birthday_animation, birthdays=birthdays, button=button)
    color_timer = Timer(100, run_animation, animation=color_cycler, animations=button_animations, button=button)
    dim_timer = Timer(50, run_animation, animation=dim, animations=button_animations, button=button)
    rainbow_timer = Timer(50, run_animation, animation=button_rainbow, animations=button_animations, button=button)
    chase_timer = Timer(50, run_animation, animation=button_chase, animations=button_animations, button=button)
    clock_timer = Timer(60000, update_clock, clock=clock)  # update every minute

    timers = [
        birthday_timer, color_timer, dim_timer,
        rainbow_timer, chase_timer, clock_timer
    ]

    while True:
        try:
            # Don't forget to call tick() for all timers
            for timer in timers:
                timer.tick()

            # And refresh the display
            displayer.display()
        except KeyboardInterrupt:
            cleanup = True
            # Hack to get the MockButtonHandler working.
            if hasattr(button, 'handle_interrupt'):
                cleanup = button.handle_interrupt()
            if cleanup:
                displayer.cleanup()
                sys.exit(0)

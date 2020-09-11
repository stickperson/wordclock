from functools import partial
import sys

from animations import ColorCycler, Pulse, RainbowGroup
from models import Clock, Timer
from settings import birthdays, display_cls, words
from button_managers import MockButtonHandler


def reset_display_and_clock(clock, displayer, **kwargs):
    displayer.reset()
    clock.update()


if __name__ == '__main__':
    # Setup clock and display
    displayer = display_cls(rows=10, columns=13, max_brightness=25)
    clock = Clock(displayer=displayer, color=None, words=words, birthdays=birthdays)

    # Update the clock immediately
    clock.update()

    # Define animations. These will be cycled through when clicking the button.
    pulse = Pulse(clock, displayer, displayer.pixels, speed=0.05, period=3)
    color_cycle = ColorCycler(clock, displayer, displayer.pixels, speed=0.05)
    birthday_animation_group = RainbowGroup(
        displayer, displayer.pixels, speed=0.05, words=[words['HAPPY'], words['BIRTHDAY']]
    )

    # These two animations should continue even after the button is released. This might be a hack but it doesn't
    # really make sense for the animation itself to care.
    # button_chase.continue_after_button_pressed = True

    # button_animations = [color_cycler, dim, button_rainbow, button_chase]
    button_animations = [pulse, color_cycle]
    button = MockButtonHandler(
        states=len(button_animations), on_reset=partial(reset_display_and_clock, clock, displayer)
    )

    # All timers.
    check_birthday_timer = Timer(60000, clock.check_birthday)  # update every minute
    update_clock_timer = Timer(60000, clock.update)  # update every minute

    timers = [check_birthday_timer, update_clock_timer]

    while True:
        cleanup = False
        try:
            # Don't forget to call tick() for all timers
            for timer in timers:
                timer.tick()

            if clock.is_birthday:
                birthday_animation_group.animate()

            # Check the state of the button
            current_state = button.current_state
            if current_state:
                button_animation = button_animations[button.current_state - 1]
                # Some animations will only be run if the button is currently pressed down. If it should be run after
                # release until the button is pressed, add `continue_after_button_pressed = True` to the animation
                # instance
                if button.is_pressed or getattr(button_animation, 'continue_after_button_pressed', False):
                    button_animation.animate()

            # And refresh the display
            displayer.display()
        except KeyboardInterrupt:
            cleanup = True
            # Hack to get the MockButtonHandler working.
            if hasattr(button, 'handle_interrupt'):
                cleanup = button.handle_interrupt()
        except Exception:  # cleanup if any uncaught exception is raised
            cleanup = True

        if cleanup:
            displayer.cleanup()
            sys.exit(0)

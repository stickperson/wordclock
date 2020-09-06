import datetime
from functools import partial
import sys

from animations import ColorCycler, Dim, Rainbow, TheaterChase
from models import Clock, Timer
from settings import birthdays, display_cls, words
from button_managers import KeyboardButtonManager


def display_birthday(now, animation, birthdays, buttons, **kwargs):
    # for button in buttons:
    #     if button.is_active:
    #         return
    month = now.month
    day = now.day
    for birthday in birthdays:
        if birthday.month == month and birthday.day == day:
            animation.update()
            return


def update_clock(now, clock, buttons, **kwargs):
    # Do not update if any button animations should override updating the clock
    for button in buttons:
        if button.is_active:
            return
    clock.update(now.hour, now.minute)


def update_display(now, displayer, **kwargs):
    displayer.display()


def reset_display_and_clock(clock, displayer):
    displayer.reset()
    now = datetime.datetime.now()
    clock.update(now.hour, now.minute)


if __name__ == '__main__':
    # Setup clock and display
    displayer = display_cls(rows=10, columns=13)
    clock = Clock(displayer=displayer, color=None, words=words)

    # Update the clock immediately
    now = datetime.datetime.now()
    clock.update(now.hour, now.minute)

    # Birthday handlers
    birthday_animation = Rainbow(displayer, words=[words['HAPPY'], words['BIRTHDAY']])

    # Define buttons and what to do when they are clicked.
    color_cycler = ColorCycler(clock, displayer)
    dim = Dim(clock, displayer)
    button_rainbow = Rainbow(displayer, words=[words['ALL']])
    button_chase = TheaterChase(displayer, words['ALL'])
    btn = KeyboardButtonManager(
        'q',
        [color_cycler, dim, button_rainbow, button_chase],
        on_reset=partial(reset_display_and_clock, clock, displayer)
    )
    buttons = [btn]

    # All timers. Unsure if timers should be used or if each class should just handle this
    birthday_timer = Timer(50, display_birthday, animation=birthday_animation, birthdays=birthdays, buttons=buttons)
    clock_timer = Timer(60000, update_clock, clock=clock, buttons=[btn])  # update every minute
    # Might not need this. Or it might not place nice with animations. Could maybe be moved into the display class
    display_timer = Timer(50, update_display, displayer=displayer)

    while True:
        try:
            birthday_timer.tick()
            btn.tick()
            clock_timer.tick()
            display_timer.tick()
        except KeyboardInterrupt:
            displayer.cleanup()
            sys.exit(0)

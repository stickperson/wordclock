import datetime
import sys

from animations import Rainbow
from models import Clock, Timer
from settings import birthdays, display_cls, words


def display_birthday(now, displayer, birthdays, **kwargs):
    month = now.month
    day = now.day
    for birthday in birthdays:
        if birthday.month == month and birthday.day == day:
            displayer.update()
            return


def update_clock(now, clock, **kwargs):
    clock.update(now.hour, now.minute)


def update_display(now, displayer, **kwargs):
    displayer.display()


if __name__ == '__main__':
    displayer = display_cls(rows=10, columns=13)
    clock = Clock(displayer=displayer, color=None, words=words)
    now = datetime.datetime.now()

    clock.update(now.hour, now.minute)

    birthday_display = Rainbow(displayer, words=[words['HAPPY'], words['BIRTHDAY']])
    birthday_timer = Timer(50, display_birthday, displayer=birthday_display, birthdays=birthdays)
    clock_timer = Timer(1000, update_clock, clock=clock)
    display_timer = Timer(50, update_display, displayer=displayer)
    while True:
        try:
            birthday_timer.tick()
            clock_timer.tick()
            display_timer.tick()
        except KeyboardInterrupt:
            displayer.cleanup()
            sys.exit(0)

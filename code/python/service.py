import datetime

from animations import Rainbow
from models import Clock, Timer
from settings import display_cls, words


def display_birthday(now, displayer=None):
    displayer.update()


if __name__ == '__main__':
    displayer = display_cls(rows=10, columns=13)
    clock = Clock(displayer=displayer, color=None, words=words)
    now = datetime.datetime.now()

    display_words = clock.determine_words(now.month, now.day, now.hour, now.minute)
    clock.update(display_words)

    birthday_display = Rainbow(displayer, words=[words['HAPPY'], words['BIRTHDAY']])
    birthday_timer = Timer(50, display_birthday, displayer=birthday_display)
    while True:
        try:
            birthday_timer.tick()
            displayer.display()
            clock.display()
        except KeyboardInterrupt:
            displayer.cleanup()

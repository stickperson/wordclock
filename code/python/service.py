import datetime

from animations import Rainbow
from models import Birthday, Clock, Timer, Word
from settings import display_cls


words = {
    'IT':       Word(start_idx=0, end_idx=1, display_value='IT'),
    'IS':       Word(start_idx=3, end_idx=4, display_value='IS'),
    'MTEN':     Word(start_idx=25, end_idx=26, display_value='TEN'),
    'HALF':     Word(start_idx=25, end_idx=26, display_value='HALF'),
    'QUARTER':  Word(start_idx=25, end_idx=26, display_value='QUARTER'),
    'TWENTY':   Word(start_idx=25, end_idx=26, display_value='TWENTY'),
    'MFIVE':    Word(start_idx=25, end_idx=26, display_value='FIVE'),
    'MINUTES':  Word(start_idx=35, end_idx=26, display_value='MINUTES'),
    'HAPPY':    Word(start_idx=6, end_idx=10, display_value='HAPPY'),
    'TO':       Word(start_idx=25, end_idx=26, display_value='TO'),
    'PAST':     Word(start_idx=25, end_idx=25, display_value='PAST'),
    'ONE':      Word(start_idx=25, end_idx=26, display_value='ONE'),
    'BIRTHDAY': Word(start_idx=12, end_idx=19, display_value='BIRTHDAY'),
    'ELEVEN':   Word(start_idx=25, end_idx=26, display_value='ELEVEN'),
    'THREE':    Word(start_idx=25, end_idx=26, display_value='THREE'),
    'SIX':      Word(start_idx=25, end_idx=26, display_value='SIX'),
    'NINE':     Word(start_idx=25, end_idx=26, display_value='NINE'),
    'FOUR':     Word(start_idx=25, end_idx=26, display_value='FOUR'),
    'SEVEN':    Word(start_idx=25, end_idx=26, display_value='SEVEN'),
    'HFIVE':    Word(start_idx=25, end_idx=26, display_value='FIVE'),
    'TWO':      Word(start_idx=25, end_idx=26, display_value='TWO'),
    'EIGHT':    Word(start_idx=25, end_idx=26, display_value='EIGHT'),
    'HTEN':     Word(start_idx=25, end_idx=26, display_value='TEN'),
    'TWELVE':   Word(start_idx=25, end_idx=26, display_value='TWELVE'),
    'OCLOCK':   Word(start_idx=25, end_idx=26, display_value='OCLOCK'),
}

def display_birthday(now, displayer=None):
    displayer.update()


if __name__ == '__main__':
    bday = Birthday(month=8, day=31)
    displayer = display_cls(rows=10, columns=13)
    clock = Clock(displayer=displayer, color=None, words=words, birthdays=[bday])
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

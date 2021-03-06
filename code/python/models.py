from dataclasses import dataclass
import datetime


class Timer:
    """
    A simple class that calls a function after a certain amount of time (in milliseconds) has
    passed. Perhaps threading.Timer would be better but this certainly works.

    delay: time in ms
    fn: function to be run
    """
    def __init__(self, delay, fn, **kwargs):
        self.delay = delay
        self.fn = fn
        self.kwargs = kwargs
        self._last_updated = None
        self._completed_initial = False

    def tick(self):
        should_update = False
        now = datetime.datetime.now()
        if not self._completed_initial:
            should_update = True
            self._completed_initial = True
        else:
            diff = now - self.last_updated
            milliseconds = diff.total_seconds() * 1000
            if milliseconds >= self.delay:
                should_update = True
        if should_update:
            self.fn(**self.kwargs)
            self.last_updated = datetime.datetime.now()


@dataclass(frozen=True)
class Birthday:
    day: int
    month: int


# Unsure if there are any good libraries for button management.
class Button:
    last_pressed: float = 0
    pressed: bool = False


@dataclass
class Word:
    start_idx: int
    end_idx: int
    display_value: str = ''


class Clock:
    def __init__(self, displayer, words, birthdays=None):
        self.displayer = displayer
        self.words = words
        self.birthdays = birthdays or []
        self._is_birthday = False

    @property
    def is_birthday(self):
        return self._is_birthday

    def check_birthday(self):
        now = datetime.datetime.now()
        month = now.month
        day = now.day
        for birthday in self.birthdays:
            if birthday.month == month and birthday.day == day:
                self._is_birthday = True
                return

    # TODO. Break into smaller functions.
    def _determine_words(self, hour, minute):
        # Determines which words to display based on the hour and minute. Could probably separate this into minutes/hours.
        hour_displays = {
            0: 'TWELVE',
            1: 'ONE',
            2: 'TWO',
            3: 'THREE',
            4: 'FOUR',
            5: 'HFIVE',
            6: 'SIX',
            7: 'SEVEN',
            8: 'EIGHT',
            9: 'NINE',
            10: 'HTEN',
            11: 'ELEVEN',
            12: 'TWELVE'
        }
        word_keys = set(['IT', 'IS', 'MINUTES'])

        if minute > 35:
            word_keys.add('TO')
        elif 5 < minute < 35:
            word_keys.add('PAST')

        if minute <= 5:
            word_keys.remove('MINUTES')
            word_keys.add('OCLOCK')
        elif 5 <= minute <= 10:
            word_keys.add('MFIVE')
        elif 11 <= minute <= 15:
            word_keys.add('MTEN')
        elif 16 <= minute <= 20:
            word_keys.remove('MINUTES')
            word_keys.add('QUARTER')
        elif 21 <= minute <= 25:
            word_keys.add('TWENTY')
        elif 25 <= minute <= 30:
            word_keys.update(['TWENTY', 'MFIVE'])
        elif 31 <= minute <= 35:
            word_keys.remove('MINUTES')
            word_keys.add('HALF')
        elif 36 <= minute <= 40:
            word_keys.update(['TWENTY', 'MFIVE'])
        elif 41 <= minute <= 45:
            word_keys.add('TWENTY')
        elif 46 <= minute <= 50:
            word_keys.remove('MINUTES')
            word_keys.add('QUARTER')
        elif 51 <= minute <= 55:
            word_keys.add('MTEN')
        elif 56 <= minute <= 60:
            word_keys.add('MFIVE')

        # Adjust the hour so 12:36 reads "25 minutes to 1"
        if minute > 35:
            hour += 1

        word_keys.add(hour_displays[hour % 12])

        words = [self.words[k] for k in word_keys]
        return words

    def update(self, *args, **kwargs):
        now = datetime.datetime.now()
        words = self._determine_words(now.hour, now.minute)
        self.displayer.clear()
        self.displayer.batch_update(words)

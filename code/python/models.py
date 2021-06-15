from dataclasses import dataclass
import datetime

from animations import Rainbow


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
        self._last_updated = 0
        self._completed_initial = False

    def tick(self):
        should_update = False
        now = datetime.datetime.now()
        if not self._completed_initial:
            should_update = True
            self._completed_initial = True
        else:
            diff = now - self._last_updated
            milliseconds = diff.total_seconds() * 1000
            if milliseconds >= self.delay:
                should_update = True
        if should_update:
            self.fn(**self.kwargs)
            self._last_updated = datetime.datetime.now()


@dataclass(frozen=True)
class Birthday:
    day: int
    month: int


@dataclass(frozen=True)
class Word:
    start_idx: int
    end_idx: int
    display_value: str = ''


# TODO: update to act as a facade to displayer
class WordClock:
    def __init__(self, display_cls, words, birthdays=None):
        self.words = words
        self.birthdays = birthdays or []
        self.displayer = display_cls(rows=10, columns=13, max_brightness=25)
        self.birthday_animation = Rainbow(
            self, self.displayer.pixels, speed=.1, words=[words['HAPPY'], words['BIRTHDAY']]
        )
        self._is_birthday = False

        self._buttons = []
        self.timers = []

        self._startup()

    def add_button(self, button):
        self._buttons.append(button)

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

    # TODO. Abstract this away to account for different languages. Some of these can be class variables as well
    def _determine_words(self, hour, minute):
        """
        Determines which words to display based on the hour and minute. Could probably separate this into minutes/hours.

        Args:
            hour (int): current hour
            minute (int): current minute

        Returns:
            set: set of Word instances
        """

        # Words to display for each 5 minute chunk.
        minute_words = [
            ('OCLOCK',),
            ('MFIVE', 'MINUTES', 'PAST'),
            ('MTEN', 'MINUTES', 'PAST'),
            ('QUARTER', 'PAST'),
            ('TWENTY', 'MINUTES', 'PAST'),
            ('TWENTY', 'MFIVE', 'MINUTES', 'PAST'),
            ('HALF', 'PAST'),
            ('TWENTY', 'MFIVE', 'MINUTES', 'TO'),
            ('TWENTY', 'MINUTES', 'TO'),
            ('QUARTER', 'TO'),
            ('MTEN', 'MINUTES', 'TO'),
            ('MFIVE', 'MINUTES', 'TO'),
        ]

        # Build up dictionary to map current minute to its appropriate 5 minute chunk
        minute_to_chunk = {}
        for minute_chunk in range(0, 60, 5):
            for m in range(minute_chunk, minute_chunk + 5):
                minute_to_chunk[m] = minute_chunk // 5

        # Always display these words
        word_keys = set(['IT', 'IS'])

        words_for_minute_chunk = minute_words[minute_to_chunk[minute]]
        word_keys.update(words_for_minute_chunk)

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

        # Adjust the hour so 12:35 reads "25 minutes to 1"
        if minute >= 35:
            hour += 1

        word_keys.add(hour_displays[hour % 12])
        words = [self.words[k] for k in word_keys]
        return words

    def cleanup(self):
        """
        Cleanup the display (turns off LEDs etc) and exits the program by default
        """
        self.displayer.cleanup()

    def update(self):
        """
        Updates the display with the current time
        """
        now = datetime.datetime.now()
        words = self._determine_words(now.hour, now.minute)
        self.displayer.clear()
        self.displayer.batch_update(words)

    def _startup(self):
        """
        Immediately fetch the time and setup button/timers
        """
        self.check_birthday()
        self.update()
        self._setup_timers()

    def reset(self):
        """
        Resets the display to default values and updates the clock.
        """
        self.displayer.reset()
        self.update()

    def _setup_timers(self):
        check_birthday_timer = Timer(60000, self.check_birthday)  # update every minute
        update_clock_timer = Timer(60000, self.update)  # update every minute

        self.timers = [check_birthday_timer, update_clock_timer]

    # TODO. Figure out how to turn off displaying the birthday animation if another animation should overwrite it.
    def tick(self):
        """
        Runs timers, checks if the birthday message should be displayed, and runs any animations
        """
        for timer in self.timers:
            timer.tick()

        if self.is_birthday and self.birthday_animation:
            self.birthday_animation.animate()

        # Check the state of all buttons. Do this here instead
        for button in self._buttons:
            button.tick()

        # And refresh the display
        self.displayer.display()

from dataclasses import dataclass
import datetime



class Timer:
    def __init__(self, delay, fn):
        self.delay = delay
        self.fn = fn
        self.last_updated = datetime.datetime.now()

    def tick(self):
        now = datetime.datetime.now()
        diff = now - self.last_updated
        milliseconds = diff.total_seconds() * 1000
        if milliseconds >= self.delay:
            self.fn()
            self.last_updated = datetime.datetime.now()


class ConsoleDisplay:
    # Display class which prints to the console for debug purposes
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def display(self, words):
        matrix = ['-' for _ in range(self.rows * self.columns)]
        for word in words:
            matrix[word.start_idx:word.end_idx+1] = word.display_value
        grid = []
        for idx in range(0, len(matrix), self.columns):
            grid.append(matrix[idx:idx+self.columns])
        
        for g in grid:
            print(g)
    

@dataclass(frozen=True)
class Birthday:
    day: int
    month: int


class Button:
    last_pressed: float = 0
    pressed: bool = False


@dataclass
class Word:
    start_idx: int
    end_idx: int
    display_value: str
    color: str = ''


class Clock:
    # TODO. Add birthdays.
    def __init__(self, displayer, color):
        self.displayer = displayer
        self.color = color

    # TODO. Break into smaller functions. Add in birthday info. TBD how to cycle colors for the birthday.
    def determine_words(self, hour, minute, possible_words):
        # Determines which words to display based on the hour and minute. Could probably separate this into minutes/hours.
        hour_displays = {
            0: 'TWELVE',
            1: 'ONE',
            2: 'TWO',
            3: 'THREE',
            4: 'FOUR',
            5: 'HFIVE',
            6: 'SIX',
            7: 'SEVEB',
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
            word_keys.add('TWENTY')
            word_keys.add('MFIVE')
        elif 31 <= minute <= 35:
            word_keys.remove('MINUTES')
            word_keys.add('HALF')
        elif 36 <= minute <= 40:
            word_keys.add('TWENTY')
            word_keys.add('MFIVE')
        elif 41 <= minute <= 45:
            word_keys.add('TWENTY')
        elif 46 <= minute <= 50:
            word_keys.remove('MINUTES')
            word_keys.add('QUARTER')
        elif 51 <= minute <= 55:
            word_keys.add('MTEN')
        elif 56 <= minute <= 60:
            word_keys.add('MFIVE')

        if minute > 35:
            hour += 1
        
        word_keys.add(hour_displays[hour % 12])

        words = [possible_words[k] for k in word_keys]
        return words

    def display_words(self, words):
        to_display = []
        for word in words:
            word.color = word.color or self.color
            to_display.append(word)
        self.displayer.display(to_display)


words = {
    'IT':       Word(start_idx=0, end_idx=1, display_value='IT'),
    'IS':       Word(start_idx=3, end_idx=4, display_value='IS'),
    'MTEN':     Word(start_idx=6, end_idx=8, display_value='TEN'),
    'HALF':     Word(start_idx=9, end_idx=12, display_value='HALF'),
    'QUARTER':  Word(start_idx=13, end_idx=19, display_value='QUARTER'),
    'TWENTY':   Word(start_idx=20, end_idx=25, display_value='TWENTY'),
    'MFIVE':    Word(start_idx=26, end_idx=29, display_value='FIVE'),
    'MINUTES':  Word(start_idx=31, end_idx=37, display_value='MINUTES'),
    'HAPPY':    Word(start_idx=39, end_idx=43, display_value='HAPPY'),
    'TO':       Word(start_idx=45, end_idx=46, display_value='TO'),
    'PAST':     Word(start_idx=48, end_idx=51, display_value='PAST'),
    'ONE':      Word(start_idx=52, end_idx=54, display_value='ONE'),
    'BIRTHDAY': Word(start_idx=56, end_idx=63, display_value='BIRTHDAY'),
    'ELEVEN':   Word(start_idx=65, end_idx=70, display_value='ELEVEN'),
    'THREE':    Word(start_idx=72, end_idx=76, display_value='THREE'),
    'SIX':      Word(start_idx=78, end_idx=80, display_value='SIX'),
    'NINE':     Word(start_idx=82, end_idx=85, display_value='NINE'),
    'FOUR':     Word(start_idx=86, end_idx=89, display_value='FOUR'),
    'SEVEN':    Word(start_idx=91, end_idx=95, display_value='SEVEN'),
    'HFIVE':    Word(start_idx=96, end_idx=99, display_value='FIVE'),
    'TWO':      Word(start_idx=100, end_idx=102, display_value='TWO'),
    'EIGHT':    Word(start_idx=105, end_idx=109, display_value='EIGHT'),
    'HTEN':     Word(start_idx=112, end_idx=114, display_value='TEN'),
    'TWELVE':   Word(start_idx=117, end_idx=122, display_value='TWELVE'),
    'OCLOCK':   Word(start_idx=124, end_idx=129, display_value='OCLOCK'),
}


if __name__ == '__main__':
    displayer = ConsoleDisplay(rows=10, columns=13)
    clock = Clock(displayer=displayer, color=None)
    now = datetime.datetime.now()

    words = clock.determine_words(now.hour, now.minute, words)
    clock.display_words(words)

    def print_hi():
        print('hi')
    print_timer = Timer(5000, print_hi)
    while True:
        print_timer.tick()

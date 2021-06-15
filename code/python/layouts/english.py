from models import Word


def setup_chunks(cls):
    minute_to_chunk = {}
    for minute_chunk in range(0, 60, 5):
        for m in range(minute_chunk, minute_chunk + 5):
            minute_to_chunk[m] = minute_chunk // 5
    setattr(cls, 'MINUTE_TO_CHUNK', minute_to_chunk)
    return cls


@setup_chunks
class EnglishLayout:
    """
    English layout like so:

    I T - I S - T E N H A L F
    Q U A R T E R T W E N T Y
    F I V E - M I N U T E S -
    H A P P Y - T O - P A S T
    O N E - B I R T H D A Y -
    E L E V E N - T H R E E -
    S I X - N I N E F O U R -
    S E V E N F I V E T W O -
    - E I G H T - - T E N - -
    T W E L V E - O C L O C K
    """
    NUM_ROWS = 10
    NUM_COLUMMS = 13
    HOUR_DISPLAYS = {
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
    MINUTE_WORDS = [
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
    WORDS = {
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
        'ALL':      Word(start_idx=0, end_idx=129)
    }

    def __init__(self) -> None:
        self.birthday_words = [self.WORDS['HAPPY'], self.WORDS['BIRTHDAY']]

    def determine_words(self, hour, minute):
        # Always display these words
        word_keys = set(['IT', 'IS'])

        words_for_minute_chunk = self.MINUTE_WORDS[self.MINUTE_TO_CHUNK[minute]]
        word_keys.update(words_for_minute_chunk)

        # Adjust the hour so 12:35 reads "25 minutes to 1"
        if minute >= 35:
            hour += 1

        word_keys.add(self.HOUR_DISPLAYS[hour % 12])
        words = [self.WORDS[k] for k in word_keys]
        return words

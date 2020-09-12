from displays.dotstar import DotstarDisplay
# from displays.console import ConsoleDisplay
from models import Birthday, Word


display_cls = DotstarDisplay
# display_cls = ConsoleDisplay


birthdays = [
    Birthday(month=9, day=11)
]

SIMULATE_KEYPRESS = True

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
    'ALL':      Word(start_idx=0, end_idx=29)
}

# words = {
#     'IT':       Word(start_idx=0, end_idx=1, display_value='IT'),
#     'IS':       Word(start_idx=3, end_idx=4, display_value='IS'),
#     'MTEN':     Word(start_idx=6, end_idx=8, display_value='TEN'),
#     'HALF':     Word(start_idx=9, end_idx=12, display_value='HALF'),
#     'QUARTER':  Word(start_idx=13, end_idx=19, display_value='QUARTER'),
#     'TWENTY':   Word(start_idx=20, end_idx=25, display_value='TWENTY'),
#     'MFIVE':    Word(start_idx=26, end_idx=29, display_value='FIVE'),
#     'MINUTES':  Word(start_idx=31, end_idx=37, display_value='MINUTES'),
#     'HAPPY':    Word(start_idx=39, end_idx=43, display_value='HAPPY'),
#     'TO':       Word(start_idx=45, end_idx=46, display_value='TO'),
#     'PAST':     Word(start_idx=48, end_idx=51, display_value='PAST'),
#     'ONE':      Word(start_idx=52, end_idx=54, display_value='ONE'),
#     'BIRTHDAY': Word(start_idx=56, end_idx=63, display_value='BIRTHDAY'),
#     'ELEVEN':   Word(start_idx=65, end_idx=70, display_value='ELEVEN'),
#     'THREE':    Word(start_idx=72, end_idx=76, display_value='THREE'),
#     'SIX':      Word(start_idx=78, end_idx=80, display_value='SIX'),
#     'NINE':     Word(start_idx=82, end_idx=85, display_value='NINE'),
#     'FOUR':     Word(start_idx=86, end_idx=89, display_value='FOUR'),
#     'SEVEN':    Word(start_idx=91, end_idx=95, display_value='SEVEN'),
#     'HFIVE':    Word(start_idx=96, end_idx=99, display_value='FIVE'),
#     'TWO':      Word(start_idx=100, end_idx=102, display_value='TWO'),
#     'EIGHT':    Word(start_idx=105, end_idx=109, display_value='EIGHT'),
#     'HTEN':     Word(start_idx=112, end_idx=114, display_value='TEN'),
#     'TWELVE':   Word(start_idx=117, end_idx=122, display_value='TWELVE'),
#     'OCLOCK':   Word(start_idx=124, end_idx=129, display_value='OCLOCK'),
#     'ALL':      Word(start_idx=0, end_idx=129)
# }

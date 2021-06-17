from wordclock.displays.console import ConsoleDisplay
from wordclock.layouts.english import EnglishLayout
from wordclock.models import Birthday


# display_cls = DotstarDisplay
layout = EnglishLayout()
display = ConsoleDisplay(layout.NUM_ROWS, layout.NUM_COLUMMS, max_brightness=25)


birthdays = [
    Birthday(month=6, day=10)
]

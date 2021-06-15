from unittest.mock import Mock
import random
import string

from rich import print as rprint
from rich.table import Table
from rich.text import Text

from .base import BaseDisplay


class ConsoleDisplay(BaseDisplay):
    """
    Display class which prints to the console for debugging purposes.

    Note: brightness is ignored.
    """
    def __init__(self, rows, columns, *args, **kwargs):
        self.pixels = Mock()
        self.rows = rows
        self.columns = columns
        self.default_color = self.current_color = (256, 0, 0)
        self.matrix = None
        self.max_brightness = self.current_brightness = 100
        self.reset()

    def clear(self):
        """
        Clears everything from the display.
        """
        self.matrix = [('-', (0, 0, 0)) for _ in range(self.rows * self.columns)]

    def reset(self):
        """
        Clears the display and resets the color to the default
        """
        self.clear()
        self.current_color = self.default_color
        self.display()

    def update_position(self, position, color=None, value=1):
        color = color or self.current_color
        self.matrix[position] = (value, color)

    def batch_update(self, words, **kwargs):
        for word in words:
            for idx in range(word.start_idx, word.end_idx + 1):
                self.update_position(idx, value=word.display_value[idx - word.start_idx], **kwargs)

    def display(self):
        grid = Table.grid(expand=False)
        [grid.add_column(justify='center') for _ in range(self.columns)]
        for idx in range(0, len(self.matrix), self.columns):
            row_data = self.matrix[idx:idx + self.columns]
            styleized_data = []
            for d in row_data:
                value, color = d
                text = Text()
                r, g, b, *_ = color  # color can have brightness, so ignore it
                text.append(f' {value} ', style=f'bold rgb({int(r)},{int(g)},{int(b)})')
                styleized_data.append(text)
            grid.add_row(*styleized_data)
        rprint(grid)

    def wheel(self, idx):
        return random.choice(string.ascii_letters)

    def cleanup(self):
        self.reset()

from unittest.mock import Mock
import random
import string

from rich import print as rprint
from rich.table import Table
from rich.text import Text


class ConsoleDisplay:
    """
    Display class which prints to the console for debugging purposes.

    Note: this does NOT work with animations.
    """
    def __init__(self, rows, columns, *args, **kwargs):
        self.pixels = Mock()
        self.rows = rows
        self.columns = columns
        self.default_color = self.current_color = (256, 0, 0)
        self.matrix = None
        self.max_brightness = self.current_brightness = 100
        self.reset()

    def reset(self):
        self.matrix = ['-' for _ in range(self.rows * self.columns)]
        self.current_color = self.default_color
        self.display()

    def update_position(self, position, color=None, value=1):
        self.matrix[position] = value

    def batch_update(self, words, **kwargs):
        for word in words:
            for idx in range(word.start_idx, word.end_idx + 1):
                self.update_position(idx, value=word.display_value[idx - word.start_idx], **kwargs)

    def display(self):
        grid = Table.grid(expand=True)
        [grid.add_column() for _ in range(self.columns)]
        for idx in range(0, len(self.matrix), self.columns):
            row_data = self.matrix[idx:idx + self.columns]
            styleized_data = []
            for d in row_data:
                text = Text()
                r, g, b = self.current_color
                text.append(d, style=f'rgb({int(r)},{int(g)},{int(b)})')
                styleized_data.append(text)
            grid.add_row(*styleized_data)
        rprint(grid)

    def wheel(self, idx):
        return random.choice(string.ascii_letters)

    def cleanup(self):
        self.reset()

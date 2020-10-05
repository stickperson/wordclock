from unittest.mock import Mock
import random
import string


class ConsoleDisplay:
    """
    Display class which prints to the console for debugging purposes.

    Note: this does NOT work with animations.
    """
    def __init__(self, rows, columns, *args, **kwargs):
        self.pixels = Mock()
        self.rows = rows
        self.columns = columns
        self.default_color = self.current_color = 'test'
        self.matrix = None
        self.max_brightness = self.current_brightness = 100
        self.reset()

    def reset(self):
        self.matrix = ['-' for _ in range(self.rows * self.columns)]

    def update_position(self, position, color=None, value=1):
        self.matrix[position] = value

    def batch_update(self, words, **kwargs):
        for word in words:
            for idx in range(word.start_idx, word.end_idx + 1):
                self.update_position(idx, value=word.display_value[idx - word.start_idx], **kwargs)

    def display(self):
        grid = []
        print('d')
        for idx in range(0, len(self.matrix), self.columns):
            grid.append(self.matrix[idx:idx+self.columns])
        print('\n')
        print('\n')
        for g in grid:
            print(g)

    def wheel(self, idx):
        return random.choice(string.ascii_letters)

    def cleanup(self):
        self.reset()

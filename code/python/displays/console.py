class ConsoleDisplay:
    """
    Display class which prints to the console for debugging purposes
    """
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = None
        self.reset()

    def reset(self):
        self.matrix = ['-' for _ in range(self.rows * self.columns)]

    def update_position(self, position, value=1):
        self.matrix[position] = value

    def batch_update(self, words):
        self.matrix = ['-' for _ in range(self.rows * self.columns)]
        for word in words:
            for idx in range(word.start_idx, word.end_idx+1):
                self.update_position(idx, word.display_value[idx - word.start_idx])

    def display(self):
        grid = []
        for idx in range(0, len(self.matrix), self.columns):
            grid.append(self.matrix[idx:idx+self.columns])
        for g in grid:
            print(g)

    def wheel(self, idx):
        return '1'
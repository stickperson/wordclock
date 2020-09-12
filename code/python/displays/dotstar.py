import adafruit_dotstar
import board


class DotstarDisplay:
    def __init__(self, rows, columns, max_brightness=100, default_color=(255, 255, 255)):
        self.pixels = adafruit_dotstar.DotStar(board.SCK, board.MOSI, rows * columns, auto_write=False)
        self.default_color = self.current_color = default_color
        self.max_brightness = self.current_brightness = max_brightness
        self.reset()

    def batch_update(self, words):
        """
        Helper function to update multiple words at once
        """
        for word in words:
            for idx in range(word.start_idx, word.end_idx + 1):
                self.update_position(idx)

    def cleanup(self):
        """
        Should only be called when we are finished
        """
        self.reset()
        self.pixels.deinit()

    # TODO. Could potentially only update if needed, but that may be difficult to implement. Unsure what the drawbacks
    # to calling this so often are.
    def display(self):
        """
        Actually displays the leds
        """
        self.pixels.show()

    def reset(self):
        """
        Makes all pixels black, resets brightness and color to what the class was initiated with
        """
        self.pixels.fill((0, 0, 0))
        self.brightness = self.max_brightness
        self.current_color = self.default_color
        self.display()

    def update_position(self, position, color=None):
        """
        Updates an individual led. Uses the current color of the display if no color is supplied.
        """
        color = color or self.current_color
        if isinstance(color, tuple):
            color = list(color)

        color.append(self.current_brightness / 100)
        self.pixels[position] = tuple(color)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

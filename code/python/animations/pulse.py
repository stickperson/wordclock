from adafruit_led_animation.animation.pulse import Pulse as AdafruitPulse


class Pulse(AdafruitPulse):
    """
    Adafruit's Pulse animation with brightness added
    """
    def __init__(self, clock, displayer, *args, words=None, **kwargs):
        super().__init__(color=displayer.current_color, *args, **kwargs)
        self.clock = clock
        self.displayer = displayer
        self.words = words

        self.change_color(self.displayer.current_color)

    def draw(self):
        color = next(self._generator)
        self.displayer.current_color = color[:3]
        scaled_brightness = color[3] * self.displayer.max_brightness
        self.displayer.current_brightness = scaled_brightness

        # If we passed in certain words only those will be updated. Otherwise, update the clock so that the brightness
        # is refreshed. This is the only way the brightness can be changed (updating the brightness on the display
        # itself will not do anything, and simply refreshing the display will not)
        if self.words:
            self.displayer.batch_update(self.words)
        else:
            self.clock.update()

    def change_color(self, color):
        self.color = color
        self.reset()

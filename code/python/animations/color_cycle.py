import colorsys

from adafruit_led_animation.animation import Animation


class ColorCycle(Animation):
    """
    Very similar to Adafruit's ColorCycle except with a different color generator function
    """
    def __init__(self, clock, displayer, *args, words=None, **kwargs):
        super().__init__(color=displayer.current_color, *args, **kwargs)
        self.clock = clock
        self.displayer = displayer
        self.words = words
        self._generator = self._color_generator()
        next(self._generator)

    def _color_generator(self):
        """
        Use HSV values to generate colors for a smoother animation
        """
        for h in range(0, 361):
            r, g, b = colorsys.hsv_to_rgb(h / 360, 1, 1)
            self._color = (r * 255, g * 255, b * 255)
            yield
        self.cycle_complete = True

    def draw(self):
        # self.displayer.current_color = self.color
        if self.words:
            self.displayer.batch_update(self.words, color=self.color)
        else:
            self.clock.update()
        next(self._generator)

import colorsys

from adafruit_led_animation.animation import Animation


class ColorCycle(Animation):
    """
    Very similar to Adafruit's ColorCycle except with a different color generator function
    """
    def __init__(self, clock, *args, words=None, **kwargs):
        super().__init__(color=clock.displayer.current_color, *args, **kwargs)
        self.clock = clock
        self.words = words
        self._generator = self._color_generator()
        next(self._generator)

    def _color_generator(self):
        """
        Use HSV values to generate colors for a smoother animation
        """
        while True:
            for h in range(0, 361):
                r, g, b = colorsys.hsv_to_rgb(h / 360, 1, 1)
                self.color = (r * 255, g * 255, b * 255)
                yield

    def draw(self):
        """
        Updates the display's color and forces a refresh of the clock. If the animation is only for particular words,
        those words are updated. Otherwise, the clock is updated as normal with new colors.
        """
        next(self._generator)
        self.clock.displayer.current_color = self.color
        if self.words:
            self.clock.displayer.batch_update(self.words, color=self.color)
        else:
            self.clock.update()

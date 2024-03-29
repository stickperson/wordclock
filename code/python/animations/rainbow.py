import colorsys

from adafruit_led_animation.animation import Animation


class Rainbow(Animation):
    """
    Fills words with a rainbow, where each letter has a different color determined by the delta
    """
    def __init__(self, clock, *args, delta=10, words=None, **kwargs):
        super().__init__(color=clock.displayer.current_color, *args, **kwargs)
        self._clock = clock
        self._words = words
        self._delta = delta

        self._colors = None
        self._iteration = 0
        self._max_idx = 359

    @property
    def colors(self):
        """
        Use HSV values to generate colors for a smoother animation
        """
        if not self._colors:
            self._colors = []
            for h in range(0, 360):
                r, g, b = colorsys.hsv_to_rgb(h / 360, 1, 1)
                self._colors.append((r * 255, g * 255, b * 255))
        return self._colors

    def draw(self):
        for word in self._words:
            for idx in range(word.end_idx + 1 - word.start_idx):
                color_idx = ((self._iteration * self._delta) + (self._delta * idx)) % self._max_idx
                color = list(self.colors[color_idx])
                color.append(self._clock.displayer.current_brightness / 100)
                try:
                    value = word.display_value[idx]
                except IndexError:
                    value = 'X'
                self._clock.displayer.update_position(
                    idx + word.start_idx,
                    color=color,
                    value=value
                )
        self._iteration += 1
        self._iteration = self._iteration % self._max_idx
        self._clock.displayer.display()

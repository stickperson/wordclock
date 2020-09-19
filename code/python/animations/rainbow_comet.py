from adafruit_led_animation.animation.rainbowcomet import RainbowComet as AdafruitRainbowComet


# TODO. Think about implementing some sort of gradient so that there are no black pixels (the tail of the comet)
class RainbowComet(AdafruitRainbowComet):
    """
    Extend's Adafruit's "RainbowComet" to update the brightness instead of color alone
    """
    def __init__(self, displayer, *args, word=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.displayer = displayer

    def draw(self):
        """
        Same exact implementation as the base class except adding in current brightness
        """
        colors = self._comet_colors
        if self.reverse:
            colors = reversed(colors)
        for pixel_no, color in enumerate(colors):
            if len(color) == 3:
                color = list(color)
                color.append(self.displayer.current_brightness / 100)

            draw_at = self._tail_start + pixel_no
            if draw_at < 0 or draw_at >= self._num_pixels:
                if not self._ring:
                    continue
                draw_at = draw_at % self._num_pixels

            self.displayer.update_position(draw_at, color=color)

        self._tail_start += self._direction

        if self._tail_start < self._left_side or self._tail_start >= self._right_side:
            if self.bounce:
                self.reverse = not self.reverse
                self._direction = -self._direction
            elif self._ring:
                self._tail_start = self._tail_start % self._num_pixels
            else:
                self.reset()
            if self.reverse == self._initial_reverse and self.draw_count > 0:
                self.cycle_complete = True

        self.displayer.display()

import colorsys

from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.pulse import Pulse as AdafruitPulse
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelSubset
from adafruit_led_animation.animation.rainbowcomet import RainbowComet as AdafruitRainbowComet


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

        if self.words:
            self.displayer.batch_update(self.words)
        else:
            self.clock.update()

    def change_color(self, color):
        self.color = color
        self.reset()


class ColorCycler(Animation):
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

    # TODO. Investiage whether FancyLED's HSV would be better
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
        self.displayer.current_color = self.color
        if self.words:
            self.displayer.batch_update(self.words)
        else:
            self.clock.update()
        next(self._generator)


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

            self.pixel_object[draw_at] = color

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


class RainbowGroup(AnimationGroup):
    # TODO. Stop hardcoding tail length
    def __init__(self, displayer, pixels, *args, sync=False, words=None, **kwargs):
        self.displayer = displayer
        members = []
        for word in words:
            subset = PixelSubset(pixels, word.start_idx, word.end_idx)
            member = RainbowComet(displayer, subset, speed=0.1, tail_length=(word.end_idx - word.start_idx + 1) * 2)
            members.append(member)
        super().__init__(*members, sync=sync)

import colorsys
import datetime


class ColorCycler:
    """
    Cycles through colors
    """

    def __init__(self, clock, displayer):
        self.clock = clock
        self.displayer = displayer
        self._color_generator = None

    def iterate_colors(self):
        for h in range(0, 361):
            r, g, b = colorsys.hsv_to_rgb(h / 360, 1, 1)
            yield (r * 255, g * 255, b * 255)

    def update(self):
        if self._color_generator is None:
            self._color_generator = self.iterate_colors()

        try:
            value = next(self._color_generator)
        except StopIteration:
            self._color_generator = self.iterate_colors()
            value = next(self._color_generator)

        now = datetime.datetime.now()
        self.displayer.current_color = value
        self.clock.update(now.hour, now.minute)


class Dim:
    """
    Dims the brightness
    """
    def __init__(self, clock, displayer):
        self.clock = clock
        self.displayer = displayer

    def update(self):
        """
        Updates the brightness of the display and also force updates the clock so the brightness is used immediately.
        """
        current_brightness = self.displayer.current_brightness
        next_brightness = current_brightness - 1
        if next_brightness < 0:
            next_brightness = self.displayer.max_brightness

        now = datetime.datetime.now()

        self.displayer.current_brightness = next_brightness
        self.clock.update(now.hour, now.minute)


class Rainbow:
    """
    Cycles through the rainbow for each word. Adapted from
    https://github.com/tinue/apa102-pi/blob/bcf98eb07576ae1f2fc61634417e2fcccc45ef11/apa102_pi/colorschemes/colorschemes.py#L88
    """
    def __init__(self, displayer, words, num_steps_per_cycle=20):
        self.displayer = displayer
        self.words = words
        self.current_step = 0
        self.num_steps_per_cycle = num_steps_per_cycle

    def _update_word(self, word):
        num_leds = word.end_idx - word.start_idx + 1
        scale_factor = 255 / num_leds  # Index change between two neighboring LEDs
        start_index = 255 / self.num_steps_per_cycle * self.current_step  # LED 0
        for i in range(num_leds):
            # Index of LED i, not rounded and not wrapped at 255
            led_index = start_index + i * scale_factor
            # Now rounded and wrapped
            led_index_rounded_wrapped = int(round(led_index, 0)) % 255
            # Get the actual color out of the wheel
            pixel_color = self.displayer.wheel(led_index_rounded_wrapped)
            self.displayer.update_position(word.start_idx + i, pixel_color)

    # TODO. Update/remove current step?
    def update(self):
        for word in self.words:
            self._update_word(word)
        self.current_step = (self.current_step + 1) % self.num_steps_per_cycle


class TheaterChase:
    """
    Runs a 'marquee' effect around the strip. Adapted from
    https://github.com/tinue/apa102-pi/blob/bcf98eb07576ae1f2fc61634417e2fcccc45ef11/apa102_pi/colorschemes/colorschemes.py#L35
    """

    def __init__(self, displayer, word, num_steps_per_cycle=2100):
        self.displayer = displayer
        self.word = word
        self.current_step = 0
        self.num_steps_per_cycle = num_steps_per_cycle
        self._last_updated = 0

    def update(self):
        # One cycle = One trip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # Note: For a smooth transition between cycles, numStepsPerCycle must
        # be a multiple of 7
        start_index = self.current_step % 7  # One segment is 2 blank, and 5 filled
        color_index = self.displayer.wheel(
            int(round(255 / self.num_steps_per_cycle * self.current_step, 0))
        )
        num_leds = self.word.end_idx - self.word.start_idx + 1
        word_start_idx = self.word.start_idx
        for idx in range(num_leds):
            # Two LEDs out of 7 are blank. At each step, the blank
            # ones move one pixel ahead.
            if ((idx + start_index) % 7 == 0) or ((idx + start_index) % 7 == 1):
                self.displayer.update_position(word_start_idx + idx, 0)
            else:
                self.displayer.update_position(word_start_idx + idx, color_index)
        self.current_step = (self.current_step + 1) % self.num_steps_per_cycle

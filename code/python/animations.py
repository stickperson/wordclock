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

    def update(self):
        for word in self.words:
            self._update_word(word)
        self.current_step += 1

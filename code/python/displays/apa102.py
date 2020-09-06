from apa102_pi.driver import apa102


class APA102Display:
    def __init__(self, rows, columns, default_color=(255, 255, 255)):
        self.strip = apa102.APA102(
            num_led=rows * columns, global_brightness=10, mosi=10, sclk=11, order='rbg'
        )
        self.default_color = self.current_color = default_color
        self.bright_percent = 100
        self.reset()

    def batch_update(self, words):
        for word in words:
            for idx in range(word.start_idx, word.end_idx+1):
                self.update_position(idx)

    def cleanup(self):
        self.reset()
        self.strip.cleanup()

    def display(self):
        self.strip.show()

    def reset(self):
        self.strip.clear_strip()
        self.brightness = 100
        self.current_color = self.default_color

    def update_position(self, position, color=None):
        color = color or self.default_color
        if isinstance(color, tuple):
            color = self.rgb_to_hex(color)
        self.strip.set_pixel_rgb(position, color, self._bright_percent)

    def wheel(self, idx):
        return self.strip.wheel(idx)

    @staticmethod
    def rgb_to_hex(rgb_tuple):
        hex_string = '0x{:02x}{:02x}{:02x}'.format(*list(rgb_tuple))
        return int(hex_string, 0)

from apa102_pi.driver import apa102


class APA102Display:
    def __init__(self, rows, columns, default_color=0xFFFFFF):
        self.strip = apa102.APA102(
            num_led=rows * columns, global_brightness=1, mosi=10, sclk=11, order='rbg'
        )
        self.default_color = default_color
        self.reset()

    def reset(self):
        self.strip.clear_strip()

    def cleanup(self):
        self.reset()
        self.strip.cleanup()

    def display(self):
        self.strip.show()

    def wheel(self, idx):
        return self.strip.wheel(idx)

    def update_position(self, position, color=None):
        color = color or self.default_color
        self.strip.set_pixel_rgb(position, color)

    def batch_update(self, words):
        for word in words:
            for idx in range(word.start_idx, word.end_idx+1):
                self.update_position(idx)

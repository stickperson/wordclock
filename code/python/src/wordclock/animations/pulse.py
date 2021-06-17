from adafruit_led_animation.animation.pulse import Pulse as AdafruitPulse
from adafruit_led_animation.helper import pulse_generator


class Pulse(AdafruitPulse):
    """
    Adafruit's Pulse animation with brightness added
    """
    def __init__(self, clock, *args, words=None, **kwargs):
        super().__init__(color=clock.displayer.current_color, *args, **kwargs)
        self.clock = clock
        self.words = words

        self.change_color(self.clock.displayer.current_color)

    def draw(self):
        color = next(self._generator)
        self.clock.displayer.current_color = color[:3]
        scaled_brightness = color[3] * self.clock.displayer.max_brightness
        self.clock.displayer.current_brightness = scaled_brightness

        # If we passed in certain words only those will be updated. Otherwise, update the clock so that the brightness
        # is refreshed. This is the only way the brightness can be changed (updating the brightness on the display
        # itself will not do anything, and simply refreshing the display will not)
        if self.words:
            self.clock.displayer.batch_update(self.words)
        else:
            self.clock.update()

    def change_color(self, color):
        self.color = color
        self.reset()

    def reset(self):
        """
        Resets the animation.
        """
        self._generator = pulse_generator(self._period, self, dotstar_pwm=True)

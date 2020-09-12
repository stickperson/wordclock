from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelSubset
from . import RainbowComet


class RainbowCometGroup(AnimationGroup):
    # TODO. Figure out what a good tail length would be
    def __init__(self, displayer, pixels, *args, sync=False, words=None, **kwargs):
        self.displayer = displayer
        members = []
        for word in words:
            subset = PixelSubset(pixels, word.start_idx, word.end_idx)
            member = RainbowComet(displayer, subset, speed=0.1, tail_length=(word.end_idx - word.start_idx + 1) * 2)
            members.append(member)
        super().__init__(*members, sync=sync)

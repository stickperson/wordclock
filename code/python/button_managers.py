import keyboard


class KeyboardButtonManager:
    def __init__(self, pin, animations, on_reset=None, *args, **kwargs):
        self.pin = pin
        self.animations = animations
        self.on_reset = on_reset
        self.animation_idx = -1
        keyboard.on_press_key(pin, self.on_press_key)

    def on_press_key(self, *args, **kwargs):
        if self.animation_idx == (len(self.animations) - 1):
            self.animation_idx = -1
            if self.on_reset:
                self.on_reset()
            return

        self.animation_idx = (self.animation_idx + 1) % len(self.animations)

    def tick(self, *args, **kwargs):
        if self.is_active:
            transition = self.animations[self.animation_idx]
            transition.update()

    @property
    def is_active(self):
        return self.animation_idx > -1

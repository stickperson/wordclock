from gpiozero import Button


class BaseButtonHandler:
    def __init__(self, *args, states=0, on_reset=None, when_pressed=None, when_released=None, **kwargs):
        self.states = states
        self.on_reset = on_reset
        self._when_pressed = when_pressed
        self._when_released = when_released

        self.current_state = 0
        self.is_pressed = False

    def when_pressed(self):
        self.is_pressed = True
        self.current_state += 1
        if self.current_state > self.states and self.on_reset:
            self.on_reset()
            self.current_state = 0
        elif self._when_pressed:
            self.when_pressed(button=self)

    def when_released(self):
        self.is_pressed = False
        if self._when_released:
            self._when_released(button=self)

    @property
    def is_active(self):
        return bool(self.current_state)


class MockButtonHandler(BaseButtonHandler):
    """
    Treats ctrl+c as a button click.
    """
    def handle_interrupt(self):
        if self.is_pressed:
            self.when_released()
        else:
            self.when_pressed()

        if self.current_state == 0:
            return True


class ButtonHandler(BaseButtonHandler):
    def __init__(self, pin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = Button(pin)
        self.button.when_held = self.when_pressed
        self.button.when_released = self.when_released

    def when_pressed(self):
        self.is_pressed = True
        self.current_state += 1
        if self.current_state > self.states and self.on_reset:
            self.on_reset()
            self.current_state = 0
        elif self._when_pressed:
            self.when_pressed()

    def when_released(self):
        self.is_pressed = False
        if self._when_released:
            self._when_released()

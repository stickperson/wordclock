import keyboard
import datetime
import settings


class KeyboardButtonManager:
    def __init__(self, pin, states=0, on_reset=None, *args, **kwargs):
        self.pin = pin
        self.states = states
        self.on_reset = on_reset

        self.current_state = 0
        self.last_updated = datetime.datetime.now()
        keyboard.on_press_key(pin, self.on_press_key)

    def on_press_key(self, *args, **kwargs):
        self.current_state += 1
        if self.current_state > self.states:
            self.current_state = 0
            if self.on_reset:
                self.on_reset()


    def tick(self, *args, **kwargs):
        # This is a hack because keyboard events are not captured over SSH.
        # See https://github.com/boppreh/keyboard/issues/195
        if getattr(settings, 'SIMULATE_KEYPRESS', False):
            now = datetime.datetime.now()
            if (now - self.last_updated).seconds >= 3:
                print('tick')
                self.last_updated = now
                self.on_press_key()

    @property
    def is_active(self):
        return bool(self.current_state)

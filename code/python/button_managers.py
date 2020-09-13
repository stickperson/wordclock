import signal

from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button as GPIOButton


class ButtonStateManager:
    def __init__(self, num_states, on_reset=None, when_held=None, when_released=None):
        self._num_states = num_states
        self.on_reset = on_reset
        self._when_held = when_held
        self._when_released = when_released

        self.current_state = 0
        self.is_pressed = False

    def when_held(self):
        self.is_pressed = True
        self.current_state += 1
        if self.current_state > self._num_states:
            self.current_state = 0
            if self.on_reset:
                self.on_reset()
        elif self._when_held:
            self.when_held(button=self)

    def when_released(self):
        self.is_pressed = False
        if self._when_released:
            self._when_released(button=self)


class BaseButton:
    def __init__(self, btn, state_manager):
        self._btn = btn
        self._state_manager = state_manager
        btn.when_held = self.when_held
        btn.when_released = self.when_released

    def when_held(self):
        print('held')
        self._state_manager.when_held()

    def when_released(self):
        self._state_manager.when_released()


class MockButton(BaseButton):
    """
    Mock button class that uses signals to catch Ctrl+C and mimics a button press.
    """
    def __init__(self, pin, state_manager, **kwargs):
        Device.pin_factory = MockFactory()
        btn = GPIOButton(pin, **kwargs)
        self.btn_pin = Device.pin_factory.pin(pin)
        self._drive_low = True
        super().__init__(btn, state_manager)
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def handle_interrupt(self, *args, **kwargs):
        """
        Switches the button state to pressed/not pressed. Sends a SIGTERM
        """
        if self._drive_low:
            self.btn_pin.drive_low()
        else:
            self.btn_pin.drive_high()

        self._drive_low = not self._drive_low


class Button(BaseButton):
    def __init__(self, pin, state_manager, **kwargs):
        btn = GPIOButton(pin, **kwargs)
        super().__init__(btn, state_manager)

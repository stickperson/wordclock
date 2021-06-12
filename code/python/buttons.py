import signal

from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button as GPIOButton


# TODO. Maybe the default state should be 1
class ButtonStateManager:
    """
    A very simple state machine that keeps track of the total number of states and resets the state to 0
    after the max was reached.
    """
    def __init__(self, num_states, on_reset=None):
        self._num_states = num_states
        self._on_reset = on_reset
        self._current_state = 0

    def increase(self):
        """
        Increases the state and resets to inactive after the max state is reached. Optionally
        calls a reset function.
        """
        self._current_state += 1
        if self._current_state > self._num_states:
            self._current_state = 0
            if self._on_reset:
                self._on_reset()


class BaseButton(GPIOButton):
    """
    Extends GPIOButton with default behavior to keep track of how many times the button has been held.
    """
    def __init__(self, pin, state_manager, when_held=None, when_released=None, tick_fn=None, **kwargs):
        """
        Initializes a button

        Args:
            pin (int): GPIO pin the button should control
            state_manager (ButtonStateManager): keeps track of how often a button is held
            when_held (function, optional): function to run when button is held. Defaults to None.
            when_released (function, optional): function to run when button is released. Defaults to None.
            tick_fn (function optional): function to run when an external source calls button.tick(), which should be
                called inside most likely a while loop. Defaults to None.
        """
        super().__init__(pin, **kwargs)
        self._state_manager = state_manager
        self.when_held = self.__button_held
        self.when_released = self.__button_released

        self.__when_held = when_held  # _when_held is already an attribute of GPIOButton
        self.__when_released = when_released  # same as _when_held
        self._tick_fn = tick_fn

    def __button_held(self):
        self._state_manager.increase()
        if self.__when_held:
            self.__when_held(self)

    def __button_released(self):
        if self.__when_released:
            self.__when_released(self)

    @property
    def current_state(self):
        return self._state_manager._current_state

    def tick(self):
        if self._tick_fn:
            self._tick_fn(self)


class MockButton(BaseButton):
    """
    Mock button class that uses signals to catch SIGINT (raised by Ctrl+C) and mimics holding/releasing a button.
    """
    def __init__(self, pin, state_manager, **kwargs):
        Device.pin_factory = MockFactory()
        # btn = GPIOButton(pin, **kwargs)
        self.btn_pin = Device.pin_factory.pin(pin)
        self._drive_low = True
        super().__init__(pin, state_manager, **kwargs)
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def handle_interrupt(self, *args, **kwargs):
        """
        Switches the button state to pressed/not pressed.
        """
        if self._drive_low:
            self.btn_pin.drive_low()
        else:
            self.btn_pin.drive_high()

        self._drive_low = not self._drive_low


class Button(BaseButton):
    def __init__(self, pin, state_manager, **kwargs):
        super().__init__(pin, state_manager, **kwargs)

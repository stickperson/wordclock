import unittest
from unittest.mock import Mock
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from wordclock.buttons import ButtonStateManager, Button, MockButton


class TestButtonStateManager:
    def test_increase_above_max_resets_counter(self):
        manager = ButtonStateManager(1)
        manager.increase()
        assert manager.current_state == 1
        manager.increase()
        assert manager.current_state == 0

    def test_increase_above_max_calls_handler(self):
        on_reset = Mock()
        manager = ButtonStateManager(1, on_reset=on_reset)
        manager.increase()
        on_reset.assert_not_called
        manager.increase()
        on_reset.assert_called_once()


class TestButton(unittest.TestCase):
    def setUp(self):
        Device.pin_factory = MockFactory()
        self.button = None

    def tearDown(self):
        """
        Close the button so the pin can be reused
        """
        self.button.close()

    def test_tick_no_tick_fn(self):
        tick_fn = Mock()
        self.button = Button(1, Mock())
        self.button.tick()
        tick_fn.assert_not_called()

    def test_tick_tick_fn(self):
        tick_fn = Mock()
        self.button = Button(1, Mock(), tick_fn=tick_fn)
        self.button.tick()
        tick_fn.assert_called_once()


class TestMockButton(unittest.TestCase):
    def tearDown(self):
        """
        Close the button so that the pin can be reused
        """
        self.button.close()

    def test_handles_interrupt(self):
        self.button = MockButton(1, Mock())
        self.button.handle_interrupt()
        assert self.button.value == 1

        self.button.handle_interrupt()
        assert self.button.value == 0

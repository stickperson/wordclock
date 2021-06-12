from unittest.mock import Mock
from buttons import ButtonStateManager


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

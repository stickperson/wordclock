import datetime
import unittest
from unittest.mock import Mock, call, patch
from models import Birthday, Timer, WordClock


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.fn = Mock()
        self.kwargs = {'hello': 'world'}
        self.timer = Timer(5000, self.fn, **self.kwargs)

    def test_should_run_fn_on_first_tick(self):
        self.timer.tick()
        self.fn.assert_called_once_with(**self.kwargs)

    def test_tick_not_run_before_delay(self):
        self.timer.tick()
        self.timer.tick()
        self.fn.assert_called_once_with(**self.kwargs)

    @patch('models.datetime')
    def test_tick_run_after_delay(self, datetime_mock):
        datetime_mock.datetime.now.side_effect = [
            datetime.datetime.now(),
            datetime.datetime.now(),
            datetime.datetime.now() + datetime.timedelta(days=1),
            datetime.datetime.now()
        ]
        self.timer.tick()
        self.timer.tick()
        assert self.fn.call_count == 2
        expected = [call(**self.kwargs), call(**self.kwargs)]
        assert self.fn.call_args_list == expected


class TestWordClockTestCase:
    display_cls = Mock()

    def test_check_birthday_true(self, words):
        now = datetime.datetime.now()
        birthday = Birthday(month=now.month, day=now.day)
        clock = WordClock(self.display_cls, words, birthdays=[birthday])
        assert clock.is_birthday is True

    def test_check_birthday_false(self, words):
        now = datetime.datetime.now()
        birthday = Birthday(month=now.month - 1, day=now.day)
        clock = WordClock(self.display_cls, words, birthdays=[birthday])
        assert clock.is_birthday is False

    @patch('models.datetime')
    def test_update_displays_current_hour(self, datetime_mock, words):
        display_cls = Mock()
        datetime_mock.datetime.now.return_value = datetime.datetime(year=2021, month=6, day=14, hour=1, minute=1)
        clock = WordClock(display_cls, words)
        clock.update()
        expected = [
            words['IS'],
            words['IT'],
            words['OCLOCK'],
            words['ONE'],
        ]
        assert display_cls.return_value.batch_update.call_count == 2
        latest_call_args = display_cls.return_value.batch_update.call_args.args[0]
        assert sorted(latest_call_args) == expected

    @patch('models.datetime')
    def test_update_displays_next_hour(self, datetime_mock, words):
        display_cls = Mock()
        datetime_mock.datetime.now.return_value = datetime.datetime(year=2021, month=6, day=14, hour=1, minute=35)
        clock = WordClock(display_cls, words)
        clock.update()
        expected = [
            words['IS'],
            words['IT'],
            words['MFIVE'],
            words['MINUTES'],
            words['TO'],
            words['TWENTY'],
            words['TWO'],
        ]
        assert display_cls.return_value.batch_update.call_count == 2
        latest_call_args = display_cls.return_value.batch_update.call_args.args[0]
        assert sorted(latest_call_args) == expected

import datetime
from unittest.mock import Mock
from models import Birthday, WordClock


class TestWordClockTestCase:
    display_cls = Mock

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

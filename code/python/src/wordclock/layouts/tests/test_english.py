from wordclock.layouts.english import EnglishLayout


class TestEnglishLayout:
    def test_update_displays_current_hour(self):
        layout = EnglishLayout()
        words = layout.determine_words(1, 1)
        expected = set([
            layout.WORDS['IS'],
            layout.WORDS['IT'],
            layout.WORDS['OCLOCK'],
            layout.WORDS['ONE'],
        ])
        assert set(words) == expected

    def test_update_displays_next_hour(self):
        layout = EnglishLayout()
        words = layout.determine_words(1, 35)
        expected = set([
            layout.WORDS['IS'],
            layout.WORDS['IT'],
            layout.WORDS['TWENTY'],
            layout.WORDS['MFIVE'],
            layout.WORDS['MINUTES'],
            layout.WORDS['TO'],
            layout.WORDS['TWO'],
        ])
        assert set(words) == expected

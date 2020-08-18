from django.test import TestCase

from core.utils.string import words_separator


class StringTestCase(TestCase):

    def test_words_separator(self):
        words = words_separator(["Monday", "Tuesday", "Friday"])
        self.assertEqual(words, "Monday, Tuesday and Friday")

        words = words_separator(["Monday", "Tuesday"])
        self.assertEqual(words, "Monday and Tuesday")

        words = words_separator(["Monday"])
        self.assertEqual(words, "Monday")

        words = words_separator([])
        self.assertEqual(words, "")

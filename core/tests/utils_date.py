from django.test import TestCase

from core.utils.date import strptime_utc_to_tz


class DateTestCase(TestCase):

    def test_strptime_utc_to_tz(self):
        dt = strptime_utc_to_tz(
            "2020-08-20 00:00:00",
            "%Y-%m-%d %H:%M:%S",
            "America/Sao_Paulo"
        )

        self.assertEqual(dt.tzinfo.zone, "America/Sao_Paulo")
        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 8)
        self.assertEqual(dt.day, 19)
        self.assertEqual(dt.hour, 21)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

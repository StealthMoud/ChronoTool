import unittest
from ChronoTool import UnixToDatetime, DatetimeToUnix

class TestChronoTool(unittest.TestCase):
    def test_unix_to_datetime(self):
        self.assertEqual(UnixToDatetime(1617235200).strip(), "2021-04-01 00:00:00")

    def test_datetime_to_unix(self):
        self.assertEqual(DatetimeToUnix("2021-04-01 00:00:00"), 1617235200)

if __name__ == "__main__":
    unittest.main()
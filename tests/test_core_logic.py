import unittest
from datetime import time

from core_logic import brightness_to_alpha, is_time_in_range


class BrightnessLogicTests(unittest.TestCase):
    def test_brightness_to_alpha_boundaries(self):
        self.assertEqual(brightness_to_alpha(100), 0)
        self.assertEqual(brightness_to_alpha(0), 255)
        self.assertEqual(brightness_to_alpha(50), 127)

    def test_brightness_to_alpha_clamps_out_of_range(self):
        self.assertEqual(brightness_to_alpha(-20), 255)
        self.assertEqual(brightness_to_alpha(120), 0)


class ScheduleLogicTests(unittest.TestCase):
    def test_non_cross_day_range(self):
        self.assertTrue(is_time_in_range(time(9, 0), time(8, 0), time(20, 0)))
        self.assertFalse(is_time_in_range(time(21, 0), time(8, 0), time(20, 0)))

    def test_cross_day_range(self):
        self.assertTrue(is_time_in_range(time(23, 0), time(22, 0), time(6, 0)))
        self.assertTrue(is_time_in_range(time(2, 0), time(22, 0), time(6, 0)))
        self.assertFalse(is_time_in_range(time(12, 0), time(22, 0), time(6, 0)))

    def test_same_start_and_end_is_full_day(self):
        self.assertTrue(is_time_in_range(time(0, 0), time(22, 0), time(22, 0)))
        self.assertTrue(is_time_in_range(time(12, 0), time(22, 0), time(22, 0)))


if __name__ == "__main__":
    unittest.main()

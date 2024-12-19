import unittest
from datetime import time
from parser import parse_open_hours
import os

class TestRestaurantParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load the actual CSV file once for all tests."""
        cls.csv_file_path = os.path.join(os.path.dirname(__file__), "restaurants.csv")

    # tests for parse_open_hours
    def test_parse_open_hours_consistent_times(self):
        """Test that parse_open_hours parses the actual CSV correctly."""
        result = parse_open_hours(self.csv_file_path)
        
        # ensure restaurant exists in the result
        self.assertIn("The Cowfish Sushi Burger Bar", result)

        # validate specific open/close hours
        expected_hours = {
            'Mon': {'open': time(11, 0), 'close': time(22, 0)},
            'Tues': {'open': time(11, 0), 'close': time(22, 0)},
            'Wed': {'open': time(11, 0), 'close': time(22, 0)},
            'Thu': {'open': time(11, 0), 'close': time(22, 0)},
            'Fri': {'open': time(11, 0), 'close': time(22, 0)},
            'Sat': {'open': time(11, 0), 'close': time(22, 0)},
            'Sun': {'open': time(11, 0), 'close': time(22, 0)},
        }

        self.assertEqual(result["The Cowfish Sushi Burger Bar"], expected_hours)

    def test_parse_open_hours_varied_times(self):
        """Test that parse_open_hours parses the actual CSV correctly."""
        result = parse_open_hours(self.csv_file_path)
        self.assertIn("Bida Manda", result)
        # Bida hours: Mon-Thu, Sun 11:30 am - 10 pm / Fri-Sat 11:30 am - 11 pm

        expected_hours = {
            'Mon': {'open': time(11, 30), 'close': time(22, 0)},
            'Tues': {'open': time(11, 30), 'close': time(22, 0)},
            'Wed': {'open': time(11, 30), 'close': time(22, 0)},
            'Thu': {'open': time(11, 30), 'close': time(22, 0)},
            'Fri': {'open': time(11, 30), 'close': time(23, 0)},
            'Sat': {'open': time(11, 30), 'close': time(23, 0)},
            'Sun': {'open': time(11, 30), 'close': time(22, 0)},
        }

        self.assertEqual(result["Bida Manda"], expected_hours)


    def test_parse_open_hours_invalid_format(self):
        """Test that invalid hour formats raise an exception."""
        invalid_csv_path = os.path.join(os.path.dirname(__file__), "invalid_hours.csv")

        # CSV with invalid time format
        with open(invalid_csv_path, "w") as f:
            f.write("Restaurant Name,Hours\n")
            f.write("Invalid Time Restaurant,Mon-Fri 25:00 am - 9:00 pm\n")  # Invalid time
        
        with self.assertRaises(ValueError):
            parse_open_hours(invalid_csv_path)


if __name__ == "__main__":
    unittest.main()

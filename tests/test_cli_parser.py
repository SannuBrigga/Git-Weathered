import unittest
from unittest.mock import patch
from weather_report import cli_parser

class TestCLIParser(unittest.TestCase):
    @patch("sys.argv", ["weather_report.py"])
    def test_missing_required_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            cli_parser()
        
        self.assertEqual(cm.exception.code, 2) # Exit code 2 for args parse error
    
    @patch("sys.argv", ["weather_report.py", "-l", "Ciudad del Este"])
    def test_handle_location(self):
        args = cli_parser()

        self.assertEqual(args.location, ["Ciudad del Este"])
    
    @patch("sys.argv", ["weather_report.py", "-l", "Ciudad del Este", "Asunción"])
    def test_handle_multiple_locations(self):
        args = cli_parser()

        self.assertEqual(len(args.location), 2)
        self.assertEqual(args.location, ["Ciudad del Este", "Asunción"])
    
    @patch("sys.argv", ["weather_report.py", "-l", "Ciudad del Este", "-f", "csv", "json", "txt"])
    def test_handle_multiple_formats(self):
        args = cli_parser()

        self.assertEqual(len(args.format), 3)
        self.assertEqual(args.format, ["csv", "json", "txt"])
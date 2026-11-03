import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import generate_daily_quote as gdq


class TestGenerateDailyQuote(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.output_file = self.temp_path / 'api' / 'today.json'
        self.history_file = self.temp_path / '.quote-history.json'

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_clean_text(self):
        self.assertEqual(gdq.clean_text('  "Hello world"  '), 'Hello world')
        self.assertEqual(gdq.clean_text('Plain text'), 'Plain text')
        self.assertEqual(gdq.clean_text('""Nested quotes""'), '"Nested quotes"')

    def test_select_quote_no_repeats(self):
        quotes = [
            {"quote": "Quote A", "author": "Author A"},
            {"quote": "Quote B", "author": "Author B"}
        ]
        history = {
            "quotes": [
                {"quote": "Quote A", "author": "Author A", "selected_on": "2099-01-01T00:00:00Z"}
            ]
        }
        selected, new_history = gdq.select_quote(quotes, history)
        self.assertEqual(selected["quote"], "Quote B")
        self.assertEqual(len(new_history["quotes"]), 2)

    def test_select_quote_resets_when_all_used(self):
        quotes = [
            {"quote": "Quote A", "author": "Author A"}
        ]
        history = {
            "quotes": [
                {"quote": "Quote A", "author": "Author A", "selected_on": "2099-01-01T00:00:00Z"}
            ]
        }
        selected, new_history = gdq.select_quote(quotes, history)
        self.assertEqual(selected["quote"], "Quote A")
        self.assertEqual(len(new_history["quotes"]), 1)

    @patch('urllib.request.urlopen')
    def test_run_with_mocked_sheet(self, mock_urlopen):
        csv_content = "Timestamp,Quote,Author\n2026-01-01,Test Quote,Test Author\n"
        mock_response = MagicMock()
        mock_response.read.return_value = csv_content.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        payload = gdq.run(
            spreadsheet_id='test-sheet',
            output_path=self.output_file,
            history_path=self.history_file
        )

        self.assertEqual(payload['quote'], 'Test Quote')
        self.assertEqual(payload['author'], 'Test Author')
        self.assertTrue(self.output_file.exists())
        self.assertTrue(self.history_file.exists())

        with open(self.output_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data['quote'], 'Test Quote')

    @patch('urllib.request.urlopen', side_effect=Exception("Network error"))
    def test_run_fallback_on_error(self, mock_urlopen):
        payload = gdq.run(
            spreadsheet_id='bad-sheet',
            output_path=self.output_file,
            history_path=self.history_file
        )
        self.assertIn(payload['quote'], [q['quote'] for q in gdq.FALLBACK_QUOTES])
        self.assertTrue(self.output_file.exists())


if __name__ == '__main__':
    unittest.main()

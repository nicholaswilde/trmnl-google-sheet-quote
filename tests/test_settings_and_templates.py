import json
import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_ruby_liquid_available() -> bool:
    if not shutil.which('ruby'):
        return False
    try:
        res = subprocess.run(
            ['ruby', '-e', "require 'liquid'"],
            capture_output=True,
            timeout=5
        )
        return res.returncode == 0
    except Exception:
        return False


HAS_RUBY_LIQUID = check_ruby_liquid_available()


class TestRegressionIssue19(unittest.TestCase):
    """Regression tests for Issue #19:

    Ensures custom Google Sheet configuration (spreadsheet_id, quote_index, author_index)
    and CSV row parsing remain fully functional across settings and all Liquid templates.
    """

    def setUp(self):
        self.settings_path = REPO_ROOT / 'src' / 'settings.yml'
        self.liquid_files = [
            'src/full.liquid',
            'src/half_horizontal.liquid',
            'src/half_vertical.liquid',
            'src/quadrant.liquid'
        ]

    def _run_ruby(self, script: str) -> subprocess.CompletedProcess:
        if not HAS_RUBY_LIQUID:
            self.skipTest("Ruby with 'liquid' gem not available in this environment")
        return subprocess.run(
            ['ruby', '-e', script],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )

    def test_regression_issue_19_settings_custom_fields_present(self):
        """Verify settings.yml contains all custom fields needed for Google Sheet configuration."""
        content = self.settings_path.read_text(encoding='utf-8')
        required_fields = [
            'spreadsheet_id',
            'quote_index',
            'author_index',
            'instructions',
            'hide_title_bar',
            'text_alignment'
        ]
        for field in required_fields:
            self.assertIn(f'keyname: {field}', content, f"Missing custom field '{field}' in settings.yml")

        self.assertIn('field_type: string', content)
        self.assertIn('default: 19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk', content)

    def test_regression_issue_19_polling_url_not_hardcoded_to_repo_json(self):
        """Verify polling_url supports both daily today.json rotation (default) and Google Sheets CSV export (custom)."""
        content = self.settings_path.read_text(encoding='utf-8')

        # Must support daily rotation via today.json for default sheet
        self.assertIn('today.json', content)
        # Must support Google Sheets CSV export for custom sheets
        self.assertIn('docs.google.com/spreadsheets/d/', content)
        self.assertIn('spreadsheet_id', content)
        self.assertIn('format=csv', content)
        self.assertIn('%Y%m%d', content)

    def test_regression_issue_19_polling_url_filter_logic_pure_python(self):
        """Verify the Liquid filter chain logic in polling_url cleanly handles all sheet ID/URL formats."""
        default_id = '19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk'

        def extract_sheet_id(val: str | None) -> str:
            s = val if val else default_id
            s = s.replace('https://docs.google.com/spreadsheets/d/', '')
            s = s.replace('http://docs.google.com/spreadsheets/d/', '')
            return s.split('/')[0].split('?')[0].split('#')[0].strip()

        test_inputs = [
            default_id,
            f'https://docs.google.com/spreadsheets/d/{default_id}/edit?usp=sharing',
            f'https://docs.google.com/spreadsheets/d/{default_id}#gid=0',
            f'https://docs.google.com/spreadsheets/d/{default_id}/',
            f'http://docs.google.com/spreadsheets/d/{default_id}/edit',
            f'  {default_id}  ',
            None,
            ''
        ]

        for input_val in test_inputs:
            extracted = extract_sheet_id(input_val)
            self.assertEqual(extracted, default_id, f"Failed extracting ID from {input_val!r}")

    def test_regression_issue_19_templates_contain_csv_parsing_logic(self):
        """Verify all Liquid templates contain the required CSV row parsing and rotation logic."""
        required_patterns = [
            r'data\.quote',
            r'data\.size\s*>\s*1',
            r'quote_index',
            r'author_index',
            r"date:\s*'%j'",
            r'data\[quote_idx\]',
            r'selected_row\[quote_col\]',
            r'selected_row\[author_col\]'
        ]

        for template_rel in self.liquid_files:
            template_path = REPO_ROOT / template_rel
            self.assertTrue(template_path.exists(), f"Template missing: {template_rel}")
            content = template_path.read_text(encoding='utf-8')
            for pat in required_patterns:
                self.assertRegex(
                    content,
                    pat,
                    f"Template {template_rel} missing pattern {pat!r} required for Google Sheets CSV parsing"
                )

    def test_regression_issue_19_rotation_bounds_never_select_header(self):
        """Verify that the day-of-year modulo formula never selects row 0 (header row) on any day."""
        for total_rows in range(2, 50):
            total_quotes = total_rows - 1
            for day in range(1, 367):
                idx = (day % total_quotes) + 1
                self.assertNotEqual(idx, 0, f"Selected header row 0 on day {day} with {total_rows} rows")
                self.assertLess(idx, total_rows, f"Index out of bounds ({idx} >= {total_rows}) on day {day}")
                self.assertGreaterEqual(idx, 1)

    def test_polling_url_supports_non_first_tab_gid(self):
        """Verify polling_url preserves &gid=XXX when user points to a specific tab per TRMNL guide."""
        ruby_script = """
        require 'yaml'
        require 'liquid'

        settings = YAML.load_file('src/settings.yml')
        tmpl = Liquid::Template.parse(settings['polling_url'])

        url_hash_gid = "https://docs.google.com/spreadsheets/d/19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk/edit#gid=987654321"
        rendered_hash = tmpl.render({ 'spreadsheet_id' => url_hash_gid })
        raise "Missing &gid=987654321 in #{rendered_hash}" unless rendered_hash.include?('&gid=987654321')

        url_query_gid = "https://docs.google.com/spreadsheets/d/19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk/edit?gid=123456789&usp=sharing"
        rendered_query = tmpl.render({ 'spreadsheet_id' => url_query_gid })
        raise "Missing &gid=123456789 in #{rendered_query}" unless rendered_query.include?('&gid=123456789')

        url_no_gid = "https://docs.google.com/spreadsheets/d/19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk"
        rendered_no_gid = tmpl.render({ 'spreadsheet_id' => url_no_gid })
        raise "Unexpected gid in #{rendered_no_gid}" if rendered_no_gid.include?('&gid=')
        raise "Expected today.json for default sheet without gid" unless rendered_no_gid.include?('today.json')

        puts 'GID_SUPPORT_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('GID_SUPPORT_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_polling_url_handles_urls(self):
        """Verify polling_url template defaults to today.json and extracts correct custom sheet ID via Liquid engine."""
        ruby_script = """
        require 'yaml'
        require 'liquid'

        settings = YAML.load_file('src/settings.yml')
        tmpl = Liquid::Template.parse(settings['polling_url'])

        default_id = '19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk'
        expected_json_url = "https://raw.githubusercontent.com/nicholaswilde/trmnl-google-sheet-quote/refs/heads/main/api/today.json"

        # Default sheet ID or empty should resolve to today.json for daily screen updates
        default_inputs = [
          default_id,
          "https://docs.google.com/spreadsheets/d/#{default_id}/edit?usp=sharing",
          "https://docs.google.com/spreadsheets/d/#{default_id}/",
          "  #{default_id}  ",
          nil,
          ''
        ]

        default_inputs.each do |input|
          rendered = tmpl.render({ 'spreadsheet_id' => input })
          raise "Failed for default input #{input.inspect}: #{rendered}" unless rendered == expected_json_url
        end

        # Custom sheet IDs should resolve to Google Sheets CSV export
        custom_id = 'custom-user-sheet-xyz'
        expected_csv_prefix = "https://docs.google.com/spreadsheets/d/#{custom_id}/export?format=csv"
        custom_inputs = [
          custom_id,
          "https://docs.google.com/spreadsheets/d/#{custom_id}/edit?usp=sharing",
          "https://docs.google.com/spreadsheets/d/#{custom_id}/",
          "  #{custom_id}  "
        ]

        custom_inputs.each do |input|
          rendered = tmpl.render({ 'spreadsheet_id' => input })
          raise "Failed for custom input #{input.inspect}: #{rendered}" unless rendered.start_with?(expected_csv_prefix)
        end

        puts 'URL_PARSING_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('URL_PARSING_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_templates_render_google_sheet_csv(self):
        """Verify all Liquid templates render quote text and author from CSV row data via Liquid engine."""
        ruby_script = f"""
        require 'liquid'

        files = {json.dumps(self.liquid_files)}
        csv_data = [
          ['Timestamp', 'Quote Text', 'Quote Author'],
          ['2026-01-01', 'Custom Sheet Quote', 'Custom Sheet Author']
        ]

        trmnl_ctx = {{
          'plugin_settings' => {{
            'custom_fields_values' => {{
              'quote_index' => 1,
              'author_index' => 2,
              'text_alignment' => 'Center',
              'hide_title_bar' => 'No'
            }}
          }}
        }}

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))
          rendered = template.render({{ 'data' => csv_data, 'trmnl' => trmnl_ctx }})
          raise "Quote missing in #{{f}}" unless rendered.include?('Custom Sheet Quote')
          raise "Author missing in #{{f}}" unless rendered.include?('Custom Sheet Author')
        end

        puts 'CSV_RENDER_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('CSV_RENDER_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_templates_custom_column_indices(self):
        """Verify Liquid templates respect custom quote_index and author_index column configurations."""
        ruby_script = f"""
        require 'liquid'

        files = {json.dumps(self.liquid_files)}
        csv_data = [
          ['Col 0 Quote', 'Col 1 Author', 'Col 2 Timestamp'],
          ['Column Zero Quote Content', 'Column One Author Name', '2026-01-01']
        ]

        trmnl_ctx = {{
          'plugin_settings' => {{
            'custom_fields_values' => {{
              'quote_index' => 0,
              'author_index' => 1
            }}
          }}
        }}

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))
          rendered = template.render({{ 'data' => csv_data, 'trmnl' => trmnl_ctx }})
          raise "Custom quote col 0 missing in #{{f}}" unless rendered.include?('Column Zero Quote Content')
          raise "Custom author col 1 missing in #{{f}}" unless rendered.include?('Column One Author Name')
        end

        puts 'CUSTOM_COLUMNS_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('CUSTOM_COLUMNS_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_templates_handle_empty_author(self):
        """Verify Liquid templates handle rows with an empty author cleanly without error or broken markup."""
        ruby_script = f"""
        require 'liquid'

        files = {json.dumps(self.liquid_files)}
        csv_data = [
          ['Timestamp', 'Quote Text', 'Quote Author'],
          ['2026-01-01', 'Anonymous Wisdom', '']
        ]

        trmnl_ctx = {{
          'plugin_settings' => {{
            'custom_fields_values' => {{
              'quote_index' => 1,
              'author_index' => 2
            }}
          }}
        }}

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))
          rendered = template.render({{ 'data' => csv_data, 'trmnl' => trmnl_ctx }})
          raise "Quote missing in #{{f}}" unless rendered.include?('Anonymous Wisdom')
          raise "Author markup should be omitted in #{{f}}" if rendered.include?('text--gray-2')
        end

        puts 'EMPTY_AUTHOR_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('EMPTY_AUTHOR_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_templates_strip_whitespace(self):
        """Verify Liquid templates strip surrounding whitespace from quote and author values."""
        ruby_script = f"""
        require 'liquid'

        files = {json.dumps(self.liquid_files)}
        csv_data = [
          ['Timestamp', 'Quote Text', 'Quote Author'],
          ['2026-01-01', '   Untrimmed Quote   ', '   Untrimmed Author   ']
        ]

        trmnl_ctx = {{
          'plugin_settings' => {{
            'custom_fields_values' => {{
              'quote_index' => 1,
              'author_index' => 2
            }}
          }}
        }}

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))
          rendered = template.render({{ 'data' => csv_data, 'trmnl' => trmnl_ctx }})
          raise "Quote not trimmed in #{{f}}" unless rendered.include?('<span>Untrimmed Quote</span>')
          raise "Author not trimmed in #{{f}}" unless rendered.include?('<span>Untrimmed Author</span>')
        end

        puts 'WHITESPACE_STRIP_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('WHITESPACE_STRIP_OK', result.stdout)

    def test_regression_issue_19_ruby_liquid_templates_backward_compatibility_json(self):
        """Verify Liquid templates retain backward compatibility with JSON payloads and empty fallback."""
        ruby_script = f"""
        require 'liquid'

        files = {json.dumps(self.liquid_files)}
        json_data = {{
          'quote' => 'JSON Quote Value',
          'author' => 'JSON Author Value'
        }}

        trmnl_ctx = {{
          'plugin_settings' => {{
            'custom_fields_values' => {{
              'quote_index' => 1,
              'author_index' => 2
            }}
          }}
        }}

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))

          # JSON render
          rendered_json = template.render({{ 'data' => json_data, 'trmnl' => trmnl_ctx }})
          raise "JSON quote failed in #{{f}}" unless rendered_json.include?('JSON Quote Value')
          raise "JSON author failed in #{{f}}" unless rendered_json.include?('JSON Author Value')

          # Fallback when data is empty
          rendered_fallback = template.render({{ 'data' => [], 'trmnl' => trmnl_ctx }})
          raise "Fallback quote failed in #{{f}}" unless rendered_fallback.include?('Steve Jobs')
        end

        puts 'BACKWARD_COMPAT_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('BACKWARD_COMPAT_OK', result.stdout)


if __name__ == '__main__':
    unittest.main()

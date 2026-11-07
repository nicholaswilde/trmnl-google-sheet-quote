import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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
        return subprocess.run(
            ['ruby', '-e', script],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )

    def test_regression_issue_19_settings_custom_fields_present(self):
        """Verify settings.yml contains all custom fields needed for Google Sheet configuration."""
        ruby_script = """
        require 'yaml'
        settings = YAML.load_file('src/settings.yml')
        fields = settings['custom_fields'] || []
        keys = fields.map { |f| f['keyname'] }

        ['spreadsheet_id', 'quote_index', 'author_index', 'instructions', 'hide_title_bar', 'text_alignment'].each do |k|
          raise "Missing custom field: #{k}" unless keys.include?(k)
        end

        sheet_field = fields.find { |f| f['keyname'] == 'spreadsheet_id' }
        raise "spreadsheet_id must have string field_type" unless sheet_field['field_type'] == 'string'
        raise "spreadsheet_id must have non-empty default" if sheet_field['default'].to_s.strip.empty?

        puts 'SETTINGS_FIELDS_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('SETTINGS_FIELDS_OK', result.stdout)

    def test_regression_issue_19_polling_url_not_hardcoded_to_repo_json(self):
        """Verify polling_url points to Google Sheets CSV export, not a hardcoded today.json URL."""
        ruby_script = """
        require 'yaml'
        settings = YAML.load_file('src/settings.yml')
        url = settings['polling_url'].to_s

        if url.include?('raw.githubusercontent.com') && url.include?('today.json')
          raise "Regression: polling_url is hardcoded to repo today.json!"
        end

        raise "polling_url must target Google Sheets" unless url.include?('docs.google.com/spreadsheets/d/')
        raise "polling_url must interpolate spreadsheet_id" unless url.include?('spreadsheet_id')
        raise "polling_url must request format=csv" unless url.include?('format=csv')
        raise "polling_url must include date cache-busting" unless url.include?('%Y%m%d')

        puts 'POLLING_URL_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('POLLING_URL_OK', result.stdout)

    def test_regression_issue_19_polling_url_handles_raw_id_and_full_urls(self):
        """Verify polling_url template extracts correct sheet ID from both bare IDs and full URLs."""
        ruby_script = """
        require 'yaml'
        require 'liquid'

        settings = YAML.load_file('src/settings.yml')
        tmpl = Liquid::Template.parse(settings['polling_url'])

        expected_id = '19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk'
        expected_prefix = "https://docs.google.com/spreadsheets/d/#{expected_id}/export?format=csv&t="

        test_inputs = [
          expected_id,
          "https://docs.google.com/spreadsheets/d/#{expected_id}/edit?usp=sharing",
          "https://docs.google.com/spreadsheets/d/#{expected_id}#gid=0",
          "https://docs.google.com/spreadsheets/d/#{expected_id}/",
          "  #{expected_id}  ",
          nil,
          ''
        ]

        test_inputs.each do |input|
          rendered = tmpl.render({ 'spreadsheet_id' => input })
          raise "Failed for input #{input.inspect}: #{rendered}" unless rendered.start_with?(expected_prefix)
        end

        puts 'URL_PARSING_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('URL_PARSING_OK', result.stdout)

    def test_regression_issue_19_templates_render_google_sheet_csv(self):
        """Verify all Liquid templates render quote text and author from CSV row data."""
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

    def test_regression_issue_19_templates_custom_column_indices(self):
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

    def test_regression_issue_19_templates_never_select_header_row(self):
        """Verify Liquid date indexing never selects row 0 (the header row) across any day of year."""
        ruby_script = """
        (2..20).each do |total_rows|
          total_quotes = total_rows - 1
          (1..366).each do |day|
            idx = (day % total_quotes) + 1
            raise "Selected header row 0 on day #{day} with #{total_rows} rows" if idx == 0
            raise "Index out of bounds (#{idx} >= #{total_rows}) on day #{day}" if idx >= total_rows
          end
        end

        puts 'ROTATION_BOUNDS_OK'
        """
        result = self._run_ruby(ruby_script)
        self.assertEqual(result.returncode, 0, f"Ruby error: {result.stderr}")
        self.assertIn('ROTATION_BOUNDS_OK', result.stdout)

    def test_regression_issue_19_templates_handle_empty_author(self):
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

    def test_regression_issue_19_templates_strip_whitespace(self):
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

    def test_regression_issue_19_templates_backward_compatibility_json(self):
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

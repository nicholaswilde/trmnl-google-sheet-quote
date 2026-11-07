import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestSettingsAndTemplates(unittest.TestCase):
    def setUp(self):
        self.settings_path = REPO_ROOT / 'src' / 'settings.yml'
        self.liquid_files = [
            REPO_ROOT / 'src' / 'full.liquid',
            REPO_ROOT / 'src' / 'half_horizontal.liquid',
            REPO_ROOT / 'src' / 'half_vertical.liquid',
            REPO_ROOT / 'src' / 'quadrant.liquid'
        ]

    def test_settings_has_required_fields(self):
        content = self.settings_path.read_text(encoding='utf-8')
        self.assertIn('spreadsheet_id', content)
        self.assertIn('quote_index', content)
        self.assertIn('author_index', content)
        self.assertIn('hide_title_bar', content)
        self.assertIn('text_alignment', content)
        self.assertIn('docs.google.com/spreadsheets/d/', content)
        self.assertIn('19hESY6AbY2ZwBph_ndF3zrw9hG__2NLzsbZTMrTlcPk', content)

    def test_liquid_templates_render_csv_and_json(self):
        ruby_script = """
        require 'liquid'
        require 'yaml'

        files = [
          'src/full.liquid',
          'src/half_horizontal.liquid',
          'src/half_vertical.liquid',
          'src/quadrant.liquid'
        ]

        csv_data = [
          ['Timestamp', 'Quote Text', 'Quote Author'],
          ['2026-01-01', 'Custom Sheet Quote', 'Custom Sheet Author']
        ]

        json_data = {
          'quote' => 'JSON Quote',
          'author' => 'JSON Author'
        }

        trmnl_ctx = {
          'plugin_settings' => {
            'custom_fields_values' => {
              'quote_index' => 1,
              'author_index' => 2,
              'text_alignment' => 'Center',
              'hide_title_bar' => 'No'
            }
          }
        }

        files.each do |f|
          template = Liquid::Template.parse(File.read(f))

          # 1. Test CSV rendering
          rendered_csv = template.render({ 'data' => csv_data, 'trmnl' => trmnl_ctx })
          raise "Failed CSV render in #{f}" unless rendered_csv.include?('Custom Sheet Quote')
          raise "Failed CSV author in #{f}" unless rendered_csv.include?('Custom Sheet Author')

          # 2. Test JSON rendering
          rendered_json = template.render({ 'data' => json_data, 'trmnl' => trmnl_ctx })
          raise "Failed JSON render in #{f}" unless rendered_json.include?('JSON Quote')
          raise "Failed JSON author in #{f}" unless rendered_json.include?('JSON Author')

          # 3. Test Fallback rendering (empty data)
          rendered_fallback = template.render({ 'data' => [], 'trmnl' => trmnl_ctx })
          raise "Failed Fallback render in #{f}" unless rendered_fallback.include?('Steve Jobs')
        end

        puts 'ALL_TEMPLATES_PASS'
        """

        result = subprocess.run(
            ['ruby', '-e', ruby_script],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Ruby script error: {result.stderr}")
        self.assertIn('ALL_TEMPLATES_PASS', result.stdout)


if __name__ == '__main__':
    unittest.main()

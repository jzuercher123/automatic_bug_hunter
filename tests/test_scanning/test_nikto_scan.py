import unittest
from unittest.mock import patch, MagicMock

from pip._internal.utils import subprocess

from src.scanning.nikto_scan import run_nikto_scan

class TestNiktoScan(unittest.TestCase):
    @patch('src.scanning.nikto_scan.subprocess.run')
    @patch('src.scanning.nikto_scan.os.makedirs')
    @patch('src.scanning.nikto_scan.open')
    def test_run_nikto_scan_success(self, mock_open, mock_makedirs, mock_run):
        # Mock subprocess.run to simulate successful Nikto execution
        mock_run.return_value = MagicMock(returncode=0)

        # Mock the open function to simulate reading JSON output
        mock_file = MagicMock()
        mock_file.read.return_value = '{"vulnerabilities": ["SQL Injection", "XSS"]}'
        mock_open.return_value.__enter__.return_value = mock_file

        result = run_nikto_scan(target='example.com', output_dir='reports/nikto/')

        self.assertEqual(result, {"vulnerabilities": ["SQL Injection", "XSS"]})
        mock_makedirs.assert_called_once_with('reports/nikto/', exist_ok=True)
        mock_run.assert_called()

    @patch('src.scanning.nikto_scan.subprocess.run')
    def test_run_nikto_scan_failure(self, mock_run):
        # Mock subprocess.run to simulate Nikto failure
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd='nikto')

        with self.assertRaises(subprocess.CalledProcessError):
            run_nikto_scan(target='example.com', output_dir='reports/nikto/')

    @patch('src.scanning.nikto_scan.subprocess.run')
    @patch('src.scanning.nikto_scan.open')
    def test_run_nikto_scan_json_parse_error(self, mock_open, mock_run):
        # Mock subprocess.run to simulate successful Nikto execution
        mock_run.return_value = MagicMock(returncode=0)

        # Mock the open function to simulate invalid JSON
        mock_file = MagicMock()
        mock_file.read.return_value = 'invalid json'
        mock_open.return_value.__enter__.return_value = mock_file

        with self.assertRaises(json.JSONDecodeError):
            run_nikto_scan(target='example.com', output_dir='reports/nikto/')

if __name__ == '__main__':
    unittest.main()

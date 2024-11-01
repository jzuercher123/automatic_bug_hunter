import unittest
from unittest.mock import patch, MagicMock
from src.scanning.nmap_scan import run_nmap_scan

class TestNmapScan(unittest.TestCase):
    @patch('src.scanning.nmap_scan.subprocess.run')
    @patch('src.scanning.nmap_scan.os.makedirs')
    @patch('src.scanning.nmap_scan.open')
    def test_run_nmap_scan_success(self, mock_open, mock_makedirs, mock_run):
        # Mock subprocess.run to simulate successful Nmap execution
        mock_run.return_value = MagicMock(returncode=0)

        # Mock the open function to simulate reading JSON output
        mock_file = MagicMock()
        mock_file.read.return_value = '{"scaninfo": "details"}'
        mock_open.return_value.__enter__.return_value = mock_file

        result = run_nmap_scan(target='example.com', output_dir='reports/nmap/')

        self.assertEqual(result, {"scaninfo": "details"})
        mock_makedirs.assert_called_once_with('reports/nmap/', exist_ok=True)
        mock_run.assert_called()

    @patch('src.scanning.nmap_scan.subprocess.run')
    def test_run_nmap_scan_failure(self, mock_run):
        # Mock subprocess.run to simulate Nmap failure
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd='nmap')

        with self.assertRaises(subprocess.CalledProcessError):
            run_nmap_scan(target='example.com', output_dir='reports/nmap/')

    @patch('src.scanning.nmap_scan.subprocess.run')
    @patch('src.scanning.nmap_scan.open')
    def test_run_nmap_scan_json_parse_error(self, mock_open, mock_run):
        # Mock subprocess.run to simulate successful Nmap execution
        mock_run.return_value = MagicMock(returncode=0)

        # Mock the open function to simulate invalid JSON
        mock_file = MagicMock()
        mock_file.read.return_value = 'invalid json'
        mock_open.return_value.__enter__.return_value = mock_file

        with self.assertRaises(json.JSONDecodeError):
            run_nmap_scan(target='example.com', output_dir='reports/nmap/')

if __name__ == '__main__':
    unittest.main()

import unittest
from src.reporting import ReportExporter
import os

class TestReportExporter(unittest.TestCase):
    def setUp(self):
        self.target = "testhost"
        self.open_ports = [(80, "Apache"), (22, "OpenSSH")]
        
    def test_html_export(self):
        """Test HTML report generation."""
        filename = "test_report.html"
        ReportExporter.export_to_html(self.target, self.open_ports, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)  # Cleanup
        
    def test_text_export(self):
        """Test text report generation."""
        filename = "test_report.txt"
        ReportExporter.export_to_text(self.target, self.open_ports, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)  # Cleanup

if __name__ == '__main__':
    unittest.main()
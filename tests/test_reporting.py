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
        
        # Check file content
        with open(filename, 'r') as f:
            content = f.read()
            self.assertIn("Port Scan Report", content)
            self.assertIn("testhost", content)
            self.assertIn("80/tcp", content)
            self.assertIn("Apache", content)
            self.assertIn("22/tcp", content)
            self.assertIn("OpenSSH", content)
        
        os.remove(filename)  # Cleanup
        
    def test_text_export(self):
        """Test text report generation."""
        filename = "test_report.txt"
        ReportExporter.export_to_text(self.target, self.open_ports, filename)
        self.assertTrue(os.path.exists(filename))
        
        # Check file content
        with open(filename, 'r') as f:
            content = f.read()
            self.assertIn("Port Scan Report for testhost", content)
            self.assertIn("80/tcp    Apache", content)
            self.assertIn("22/tcp    OpenSSH", content)
        
        os.remove(filename)  # Cleanup
        
    def test_pdf_export(self):
        """Test PDF report generation."""
        filename = "test_report.pdf"
        ReportExporter.export_to_pdf(self.target, self.open_ports, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)  # Cleanup

if __name__ == '__main__':
    unittest.main()
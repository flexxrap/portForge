import unittest
from unittest.mock import patch, MagicMock
import socket
from src.scanner import PortScanner

class TestPortScanner(unittest.TestCase):
    def setUp(self):
        self.target = "127.0.0.1"
        self.port_range = (80, 80)
        self.scanner = PortScanner(self.target, self.port_range)
    
    @patch('src.scanner.socket.socket')
    def test_scan_port_open(self, mock_socket):
        """Test scanning an open port."""
        # Mock socket connection to return success (0)
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.connect_ex.return_value = 0
        mock_socket_instance.recv.return_value = b"HTTP/1.1 200 OK\r\nServer: Test"
        
        self.scanner.scan_port(80)
        
        # Verify port was added to open_ports
        self.assertEqual(len(self.scanner.open_ports), 1)
        self.assertEqual(self.scanner.open_ports[0][0], 80)
        self.assertIn("HTTP/1.1 200 OK", self.scanner.open_ports[0][1])
    
    @patch('src.scanner.socket.socket')
    def test_scan_port_closed(self, mock_socket):
        """Test scanning a closed port."""
        # Mock socket connection to return failure (1)
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.connect_ex.return_value = 1
        
        self.scanner.scan_port(80)
        
        # Verify no ports were added to open_ports
        self.assertEqual(len(self.scanner.open_ports), 0)
    
    @patch('src.scanner.socket.socket')
    def test_grab_banner_http(self, mock_socket):
        """Test banner grabbing for HTTP service."""
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = b"HTTP/1.1 200 OK\r\nServer: Apache"
        
        banner = self.scanner._grab_banner(mock_socket_instance, 80)
        
        self.assertIn("HTTP/1.1 200 OK", banner)
    
    def test_grab_banner_unknown_service(self):
        """Test banner grabbing for unknown service."""
        with patch('src.scanner.socket.socket') as mock_socket:
            mock_socket_instance = mock_socket.return_value.__enter__.return_value
            mock_socket_instance.recv.return_value = b""
            
            banner = self.scanner._grab_banner(mock_socket_instance, 12345)
            
            self.assertEqual(banner, "Unknown")

if __name__ == '__main__':
    unittest.main()